"""Arranque y branding global del seed (no destinado a edición de product teams).

Aquí vivís valores de marca compartidos: título de ventana combinado con la página actual,
icono emoji o ruta, descripción/meta (mejor esfuerzo en SPA) y el CSS global del seed.

Streamlit sólo garantiza `:title`/favicon vía API; `<meta>` inyectadas vía marcado llegan al
árbol DOM de React (no necesariamente `<head>`). Para previews sociales tipo Link unfurl hay
habitualmente que parchear `streamlit/static/index.html` en build de imagen."""

from __future__ import annotations

import html as html_escape
from collections.abc import Iterable
from pathlib import Path

import streamlit as st

from seed_ui import inject_base_css

_APP_ROOT = Path(__file__).resolve().parent

# --- Mantenedor del seed solo (no producto día a día) ---
PLATFORM_APP_TITLE = "Boogiepop Streamlit Seed"
PLATFORM_DEFAULT_META_DESCRIPTION = (
    "Plantilla multipágina lista para ECS: páginas, estado de sesión, cachés y Docker→ECR."
)
DEFAULT_META_TAGS: tuple[dict[str, str], ...] = (
    {"name": "author", "content": "Boogiepop"},
)

# Sobrescribe en PR de plataforma si necesitás snippets globales más allá de `styles/base.css`.
EXTRA_GLOBAL_MAINTAINER_CSS = ""


def configure_page(
    *,
    title: str,
    page_icon: str | Path | None = "🌱",
    combine_title_suffix: bool = True,
    meta_description: str | None = None,
    extra_meta_attrs: Iterable[dict[str, str]] | None = None,
    inject_seed_styles: bool = True,
    layout: str = "wide",
    initial_sidebar_state: str = "expanded",
) -> None:
    """Debe ejecutarse antes que cualquier otra llamada Streamlit (`st.`).

    Parámetros
    ----------
    title
        Título corto de la página actual dentro del seed.
    page_icon
        Emoji, URL o archivo relativo dentro de ``app/`` interpretado como PNG/SVG conocido por Streamlit.
    combine_title_suffix
        Cuando está activado, arma ``"{title} · {PLATFORM_APP_TITLE}"`` como título visible en la pestaña.
    meta_description
        Texto opcional (<meta name="description">); ``None`` reutiliza la descripción de plataforma.
    extra_meta_attrs
        Lista de diccionarios de atributos para armar etiquetas `<meta ... />` (ej. OpenGraph).
        Usá sólo texto ASCII seguro cuando sea posible.
    """

    merged_title = f"{title} · {PLATFORM_APP_TITLE}" if combine_title_suffix else title
    resolved_icon = _resolve_icon_arg(page_icon)
    kwargs: dict[str, object] = {
        "page_title": merged_title,
        "layout": layout,
        "initial_sidebar_state": initial_sidebar_state,
    }
    if resolved_icon is not None:
        kwargs["page_icon"] = resolved_icon

    st.set_page_config(**kwargs)

    if inject_seed_styles:
        inject_base_css()
        if EXTRA_GLOBAL_MAINTAINER_CSS.strip():
            st.markdown(f"<style>{EXTRA_GLOBAL_MAINTAINER_CSS}</style>", unsafe_allow_html=True)

    fingerprint = (
        merged_title,
        meta_description if meta_description is not None else PLATFORM_DEFAULT_META_DESCRIPTION,
        tuple(_normalize_meta_specs(extra_meta_attrs)),
    )
    prior = st.session_state.get("_seed_main_meta_fingerprint")
    if prior != fingerprint:
        _inject_meta_tags(
            description=meta_description if meta_description is not None else PLATFORM_DEFAULT_META_DESCRIPTION,
            extra=extra_meta_attrs,
        )
        st.session_state["_seed_main_meta_fingerprint"] = fingerprint


def _resolve_icon_arg(icon: str | Path | None) -> str | Path | None:
    if icon is None:
        return None
    if isinstance(icon, Path):
        candidate = icon if icon.is_absolute() else _APP_ROOT / icon
        if candidate.exists():
            return candidate
        return icon

    icon_str = str(icon)
    lowered = icon_str.lower()
    if lowered.startswith(("http://", "https://")):
        return icon_str
    if lowered.startswith(":"):
        # Streamlit permite iconografía tipo :material/info:
        return icon_str
    suffixes = (".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg", ".gif")
    if lowered.endswith(suffixes):
        candidate = Path(icon_str)
        resolved = candidate if candidate.is_absolute() else _APP_ROOT / candidate
        if resolved.exists():
            return resolved
        return icon_str
    # Por defecto: emoji textual u otro literal soportado por Streamlit.
    return icon_str


def _normalize_meta_specs(extra_meta_attrs: Iterable[dict[str, str]] | None) -> tuple[frozenset[tuple[str, str]], ...]:
    specs: list[frozenset[tuple[str, str]]] = []
    extras = tuple(extra_meta_attrs or ())
    merged = [*DEFAULT_META_TAGS, *extras]
    for attrs in merged:
        items = tuple(sorted(attrs.items()))
        specs.append(frozenset(items))
    return tuple(specs)


def _inject_meta_tags(
    *,
    description: str,
    extra: Iterable[dict[str, str]] | None,
) -> None:
    blobs: list[str] = []

    blobs.append(_meta_html({"name": "description", "content": description}))

    extras = tuple(extra or ())
    merged = [*DEFAULT_META_TAGS, *extras]
    for attrs in merged:
        blobs.append(_meta_html(attrs))

    st.markdown("\n".join(blobs), unsafe_allow_html=True)


def _meta_html(attrs: dict[str, str]) -> str:
    parts: list[str] = []
    for key, raw in attrs.items():
        escaped_key = html_escape.escape(str(key), quote=False)
        escaped_val = html_escape.escape(str(raw), quote=True)
        parts.append(f'{escaped_key}="{escaped_val}"')
    return "<meta " + " ".join(parts) + " />"

