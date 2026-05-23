"""Utilidades UI mínimas del seed (CSS, patrones repetibles)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def inject_base_css() -> None:
    """Inyecta `styles/base.css` una vez por sesión de navegador.

    Mantener el alcance limitado (.seed-*) para no depender del DOM interno de Streamlit.
    """
    if st.session_state.get("_seed_css_injected"):
        return

    css_path = Path(__file__).resolve().parent / "styles" / "base.css"
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.session_state["_seed_css_injected"] = True


def hero_card(title: str, subtitle: str) -> None:
    inject_base_css()
    st.markdown(
        f'<div class="seed-hero-card"><h2 style="margin:0">{title}</h2>'
        f'<p style="margin:0.35rem 0 0">{subtitle}</p></div>',
        unsafe_allow_html=True,
    )
