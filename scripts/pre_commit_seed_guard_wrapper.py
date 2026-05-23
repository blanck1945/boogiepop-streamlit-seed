"""Wrapper ejecutado por `pre-commit` para comparar rutas staged."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    files = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"],
        cwd=ROOT,
        text=True,
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_protected_paths.py"),
            "--stdin",
            "--manifest",
            "maintainers/seed-protected-paths.txt",
        ],
        cwd=ROOT,
        input=files,
        text=True,
    )
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
