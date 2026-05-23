"""Demo interactivo: `st.session_state`, `st.cache_data` y `st.cache_resource`."""

from __future__ import annotations

import time

import streamlit as st

from seed_main import PLATFORM_APP_TITLE, configure_page

configure_page(
    title="Demo estado y cachés",
    page_icon="⚡",
    extra_meta_attrs=(
        {"property": "og:type", "content": "article"},
        {"property": "og:title", "content": f"{PLATFORM_APP_TITLE}: demo estado y cachés"},
    ),
)

st.title("Demo: estado de sesión y cachés")


def expensive_io_query(delay_s: float = 0.4) -> str:
    time.sleep(delay_s)
    return f"resultado después de {delay_s}s"


@st.cache_data(ttl=30, show_spinner=False)
def load_dataset_like(name: str) -> str:
    """Simula datos serializables (CSV, APIs idempotentes, etc.)."""
    # name entra en la clave de caché: distintos nombres = distintos resultados cacheados.
    _ = expensive_io_query(0.35)
    return f"dataset «{name}» (TTL 30s)"


@st.cache_resource
def expensive_client_like() -> str:
    """Simula recurso pesado global (motor SQL, modelo en GPU, cliente HTTP reusable)."""
    _ = expensive_io_query(0.5)
    return "cliente simulado (una instancia por proceso)"


st.markdown(
    "### `st.session_state`"
    '\nPersiste valores **por usuario y sesión** mientras la app corre. '
    "Ideal para filtros UI, drafts y flags de una sola página."
)

if "demo_counter" not in st.session_state:
    st.session_state.demo_counter = 0

c1, c2 = st.columns(2)
with c1:
    if st.button("Incrementar contador"):
        st.session_state.demo_counter += 1
with c2:
    if st.button("Reiniciar contador"):
        st.session_state.demo_counter = 0

st.metric("Contador en sesión", st.session_state.demo_counter)

name = st.text_input("Nombre de dataset para la caché", value="demo", key="dataset_name_demo")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### `st.cache_data`")
    st.caption("Datos reproducibles desde inputs serializables. Invalidá con TTL o `clear()`.")
    if st.button("Forzar nueva lectura (cache bust)"):
        load_dataset_like.clear()

    with st.spinner("Primera llamada será lenta; las siguientes leen desde caché…"):
        st.success(load_dataset_like(name))

with col_b:
    st.markdown("### `st.cache_resource`")
    st.caption("Recursos singleton por proceso Worker; no TTL por defecto.")
    if st.button("Recrear recurso"):
        expensive_client_like.clear()

    with st.spinner("Inicialización del recurso…"):
        st.info(expensive_client_like())
