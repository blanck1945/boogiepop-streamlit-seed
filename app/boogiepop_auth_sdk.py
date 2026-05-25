"""SDK de autenticación para remotes: sin login, sólo resolución de sesión/roles.

Patrón recomendado:
- El host hace login y entrega un token al remote (query param, header invertido o state propio).
- Este SDK consume `GET /api/auth/me` para hidratar identidad y roles.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any, Mapping, Sequence
from urllib import error, request

import streamlit as st


@dataclass(frozen=True)
class BoogiepopUser:
    id: str
    name: str
    email: str


@dataclass(frozen=True)
class BoogiepopSessionSnapshot:
    user: BoogiepopUser | None
    roles: tuple[str, ...]
    token: str | None
    source: str
    error: str | None


def _first_str(value: Any) -> str | None:
    if isinstance(value, str):
        trimmed = value.strip()
        return trimmed or None
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for item in value:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return None


def _derive_name_from_email(email: str) -> str:
    local = email.split("@", 1)[0].strip()
    return local or "user"


def _resolve_api_base(explicit: str | None = None) -> str | None:
    chosen = (explicit or "").strip() or os.getenv("BOOGIEPOP_API_BASE_URL", "").strip()
    if not chosen:
        return None
    return chosen.rstrip("/")


def _get_token_from_query(query_param_key: str) -> str | None:
    return _first_str(st.query_params.get(query_param_key))


def _fetch_auth_me(token: str, api_base: str, timeout_seconds: float) -> Mapping[str, Any]:
    req = request.Request(
        f"{api_base}/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            payload = response.read().decode("utf-8")
            parsed = json.loads(payload)
            if not isinstance(parsed, dict):
                raise ValueError("Respuesta inválida de /api/auth/me")
            return parsed
    except error.HTTPError as exc:
        raise RuntimeError(f"No se pudo leer /api/auth/me ({exc.code})") from exc
    except error.URLError as exc:
        raise RuntimeError("No se pudo conectar con Boogiepop API") from exc


def resolve_boogiepop_session(
    *,
    token: str | None = None,
    api_base_url: str | None = None,
    token_query_param_key: str = "bpToken",
    timeout_seconds: float = 5.0,
) -> BoogiepopSessionSnapshot:
    resolved_token = (token or "").strip() or _get_token_from_query(token_query_param_key)
    if not resolved_token:
        return BoogiepopSessionSnapshot(
            user=None,
            roles=(),
            token=None,
            source="none",
            error=None,
        )

    api_base = _resolve_api_base(api_base_url)
    if not api_base:
        return BoogiepopSessionSnapshot(
            user=None,
            roles=(),
            token=resolved_token,
            source="token-only",
            error="BOOGIEPOP_API_BASE_URL no configurada para /api/auth/me",
        )

    try:
        me = _fetch_auth_me(resolved_token, api_base, timeout_seconds)
        email = str(me.get("email") or "").strip()
        if not email:
            raise RuntimeError("Respuesta inválida de /api/auth/me: falta email")

        user_id = str(me.get("userId") or "unknown").strip() or "unknown"
        roles_raw = me.get("roles")
        roles: tuple[str, ...] = ()
        if isinstance(roles_raw, list):
            roles = tuple(str(role).strip() for role in roles_raw if str(role).strip())

        return BoogiepopSessionSnapshot(
            user=BoogiepopUser(id=user_id, name=_derive_name_from_email(email), email=email),
            roles=roles,
            token=resolved_token,
            source="token+me",
            error=None,
        )
    except Exception as exc:
        return BoogiepopSessionSnapshot(
            user=None,
            roles=(),
            token=resolved_token,
            source="token-only",
            error=str(exc),
        )


def has_role(snapshot: BoogiepopSessionSnapshot | None, expected: str) -> bool:
    normalized = expected.strip().lower()
    if not normalized:
        return False
    roles = snapshot.roles if snapshot else ()
    return any(role.strip().lower() == normalized for role in roles)


def has_any_role(snapshot: BoogiepopSessionSnapshot | None, expected_roles: Sequence[str]) -> bool:
    valid_expected = [role.strip() for role in expected_roles if role.strip()]
    if not valid_expected:
        return True
    return any(has_role(snapshot, expected) for expected in valid_expected)
