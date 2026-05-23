"""Punto de entrada de la app Streamlit multipágina."""

from __future__ import annotations

import streamlit as st

from seed_main import PLATFORM_APP_TITLE, configure_page
from seed_ui import hero_card

configure_page(
    title="Inicio",
    page_icon="🌱",
    extra_meta_attrs=(
        {"property": "og:type", "content": "website"},
        {"property": "og:title", "content": PLATFORM_APP_TITLE},
    ),
)
hero_card(
    "Boogiepop Streamlit Seed",
    "Plantilla multipágina lista para ECS: tema, páginas, sesión y cachés.",
)

st.markdown(
    "Usá el menú lateral para navegar entre **Demo** "
    "(estado + cachés) y **Sobre el seed** (guía)."
)
st.markdown('<p class="seed-muted">Ejecutá localmente: <code>streamlit run Home.py</code> desde la carpeta <code>app/</code>.</p>', unsafe_allow_html=True)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.subheader("Páginas incluidas")
    st.page_link(
        "pages/01_Demo_estado_y_cache.py",
        label="Demo: estado de sesión y cachés",
        icon="⚡",
    )
    st.page_link(
        "pages/02_Sobre_el_seed.py",
        label="Sobre este seed",
        icon="📚",
    )
with c2:
    st.subheader("Siguientes pasos")
    st.markdown(
        "- Revisá el archivo **`AGENTS.md`** en la raíz del repositorio "
        "(guía para desarrolladores y agentes automatizados).\n"
        "- Construí la imagen Docker y publícala en ECR antes de ECS (consultá el README)."
    )
