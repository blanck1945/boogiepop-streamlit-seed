#!/usr/bin/env python3
"""Checks changed repository paths against the seed infra manifest."""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from pathlib import PurePosixPath
from typing import Iterable


def parse_manifest(lines: list[str]) -> list[str]:
    globs: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        globs.append(line)
    return globs


def load_manifest(path: str) -> list[str]:
    with open(path, encoding="utf-8") as handle:
        return parse_manifest(handle.readlines())


def normalize_path(candidate: str) -> str:
    p = PurePosixPath(candidate.replace("\\", "/"))
    posix = str(p.as_posix())
    if posix.startswith("../"):
        posix = posix.replace("../", "").lstrip("/")
    posix = posix.lstrip("./").lstrip("/")
    while posix.startswith("./"):
        posix = posix.removeprefix("./")
    return posix


def path_matches(candidate: str, pattern: str) -> bool:
    norm = normalize_path(candidate)
    if pattern.endswith("/**"):
        prefix = normalize_path(pattern[:-3]).rstrip("/")
        return norm.startswith(f"{prefix}/") or norm == prefix
    norm_pattern = normalize_path(pattern)
    plain = "*" not in norm_pattern and "?" not in norm_pattern and "[" not in norm_pattern
    if plain:
        return norm == norm_pattern
    return fnmatch.fnmatch(norm, norm_pattern)


def filter_protected(paths: Iterable[str], patterns: list[str]) -> list[str]:
    offending: dict[str, None] = {}
    seen: dict[str, None] = {}

    for raw in paths:
        norm = normalize_path(raw)
        if not norm or norm in seen:
            continue
        seen[norm] = None
        if any(path_matches(norm, pattern) for pattern in patterns):
            offending[norm] = None

    return sorted(offending.keys())


def git_rev_parse(repo_root: str, revision: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", repo_root, "rev-parse", "--verify", revision],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()




def git_merge_paths(repo_root: str, lhs: str, rhs: str) -> list[str]:
    merge_proc = subprocess.run(
        ["git", "-C", repo_root, "merge-base", lhs, rhs],
        check=False,
        capture_output=True,
        text=True,
    )
    if merge_proc.returncode != 0:
        raise RuntimeError(
            "No se pudo calcular merge-base para "
            f"{lhs!r} y {rhs!r}: {merge_proc.stderr.strip()}",
        )
    merge_base = merge_proc.stdout.strip()
    cmd = subprocess.run(
        ["git", "-C", repo_root, "diff", "--name-only", merge_base, rhs],
        check=False,
        capture_output=True,
        text=True,
    )
    if cmd.returncode != 0:
        raise RuntimeError(cmd.stderr.strip())
    return [ln.strip() for ln in cmd.stdout.splitlines() if ln.strip()]


def should_bypass_via_env() -> bool:
    flag = (os.environ.get("SEED_INFRA_CI_FLAG") or "").strip()
    if flag == "1":
        print(
            "SEED_INFRA_CI_FLAG=1 activado vía CI/CD masked+protected sólo equipo plataforma.",
            file=sys.stderr,
        )
        return True
    bypass_token = (os.environ.get("SEED_INFRA_CI_BYPASS_TOKEN") or "").strip()
    expected = (os.environ.get("SEED_INFRA_CI_BYPASS_EXPECTED") or "").strip()
    if bypass_token and expected and bypass_token == expected:
        return True
    if os.environ.get("SEED_GUARD_BYPASS") == "1":
        print(
            "SEED_GUARD_BYPASS=1 activo; sólo usar en equipos mantenedores conscientes.",
            file=sys.stderr,
        )
        return True
    return False


def should_bypass_mr_label() -> bool:
    labels_raw = os.environ.get("CI_MERGE_REQUEST_LABELS") or ""
    lowered = labels_raw.casefold()
    lowered_no_space = lowered.replace(" ", "").replace(",", "")
    return "seed-infra-approved".casefold() in lowered_no_space


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default="maintainers/seed-protected-paths.txt",
        help="Lista de patrons protegidos",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Leer rutas modificadas línea por línea desde stdin (hook pre-commit)",
    )
    parser.add_argument("--repository", default=".", help="Raíz git del proyecto")

    git_group = parser.add_argument_group("git diff modo CI/local")
    git_group.add_argument(
        "--from-ref",
        help="Commit base típico (CI_MERGE_REQUEST_DIFF_BASE_SHA o branch default)",
    )
    git_group.add_argument(
        "--to-ref",
        help="HEAD destino típico (CI_COMMIT_SHA o HEAD)",
    )

    args = parser.parse_args(argv)

    repo_root = os.path.abspath(args.repository)
    manifest_abs = (
        os.path.abspath(args.manifest)
        if os.path.isabs(args.manifest)
        else os.path.join(repo_root, args.manifest)
    )

    if not os.path.isfile(manifest_abs):
        raise SystemExit(f"No existe manifest infra: {manifest_abs}")

    patterns = load_manifest(manifest_abs)

    if should_bypass_via_env() or should_bypass_mr_label():
        print("Bypass infra seed activo — chequeo omitido.", file=sys.stderr)
        return 0

    if args.stdin:
        incoming = sys.stdin.read().splitlines()
    elif args.from_ref and args.to_ref:
        lhs = git_rev_parse(repo_root, args.from_ref)
        rhs = git_rev_parse(repo_root, args.to_ref)
        if lhs is None or rhs is None:
            raise SystemExit(f"Refs inválidas: from={args.from_ref!r} to={args.to_ref!r}")
        incoming = git_merge_paths(repo_root, lhs, rhs)
    else:
        parser.error("--stdin O ambos --from-ref / --to-ref son necesarios.")

    hits = filter_protected(incoming, patterns)

    if not hits:
        print("Sin cambios en rutas protegidas del seed (ok)")
        return 0

    print(
        "::error Este cambio toca infra protegida del seed "
        "(ver maintainers/README.md y AGENTS.md).",
        file=sys.stderr,
    )
    print("Rutas bloqueadas:")
    for item in hits:
        print(f" - {item}")
    print()
    print("Bypass coordinado equipo plataforma:")
    print("- Etiqueta MR GitLab: seed-infra-approved")
    print("- CI masked+protected: SEED_INFRA_CI_FLAG=1 (recomendado)")
    print("- Alternativa: SEED_INFRA_CI_BYPASS_TOKEN == SEED_INFRA_CI_BYPASS_EXPECTED")
    print("- Solo desarrollo mantenedor local: SEED_GUARD_BYPASS=1 (spoofeable)")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(130) from None
