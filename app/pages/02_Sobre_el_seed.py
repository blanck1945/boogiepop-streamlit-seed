"""Documentación in-app sobre el contenido del seed."""

from __future__ import annotations

import streamlit as st

from seed_main import PLATFORM_APP_TITLE, configure_page

configure_page(
    title="Sobre el seed",
    page_icon="📚",
    extra_meta_attrs=(
        {"property": "og:type", "content": "website"},
        {"property": "og:title", "content": f"{PLATFORM_APP_TITLE}: guía del seed"},
    ),
)

st.title("Sobre este seed")
st.markdown(
    '<p class="seed-muted">Resumen vivo de convenciones, estilos, multipágina '
    "y uso de estado/cachés. Para reglas orientadas a agentes, véase "
    "<code>AGENTS.md</code> en la raíz del repositorio.</p>",
    unsafe_allow_html=True,
)

tab_css, tab_pages, tab_session = st.tabs(
    ["CSS y tema", "Multipágina (pages)", "Sesión y cachés"]
)

with tab_css:
    st.subheader("Tema Streamlit (`config.toml`)")
    st.markdown(
        "El tema base vive en `app/.streamlit/config.toml`: colores, fuente "
        "`sans serif`, y servidor headless pensado para contenedores."
    )
    st.code(
        '''[theme]
base = "light"
primaryColor = "#4361ee"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f4f8"
textColor = "#1a1a2e"
font = "sans serif"
''',
        language="toml",
    )
    st.subheader("CSS adicional (`app/styles/base.css`)")
    st.markdown(
        "- Usá prefijos `.seed-*` para no pisar widgets internos de Streamlit.\n"
        "- El archivo `seed_main.py` ejecuta **`configure_page(...)`, que debe ser tu primera llamada `st.*`** y dentro "
        'llama a `seed_ui.inject_base_css()` usando la clave `session_state["_seed_css_injected"]` para cargar sólo '
        'una vez el CSS durante la navegación.\n'
        "- Podés concatenar snippets adicionales del equipo de plataforma con "
        '`EXTRA_GLOBAL_MAINTAINER_CSS` dentro de ese mismo archivo (no es para trabajo diario).\n'
        '- Evitá hacks directos contra el DOM de Streamlit.'
    )
    st.code(
        """from seed_main import configure_page

configure_page(title=\"Inicio\", page_icon=\"🌱\")  # debe ir primero
""",
        language="python",
    )


with tab_pages:
    st.subheader("Convención de archivos en `pages/`")
    st.markdown(
        "- Nombren archivos como `NN_Título_snake_case.py`.\n"
        "- El número `NN` controla **orden en la barra lateral**.\n"
        "- Importá código compartido desde el paquete bajo `app/` (este seed usa rutas relativas cuando corrés desde `app/`)."
    )
    st.code(
        '''from seed_main import configure_page

configure_page(title="Mi página", page_icon="⚡")


st.title("…")
''',
        language="python",
    )

with tab_session:
    st.subheader("`st.session_state`")
    st.markdown(
        "Estado **por navegador y sesión**; se pierde al cerrar pestaña/recargar duro "
        "(según servidor). Preferí claves prefijadas (p. ej. `demo_*`) si compartís módulos."
    )
    st.subheader("`st.cache_data` vs `st.cache_resource`")
    st.markdown(
        "| Decorador | Usá cuando… |\n|---|---|\n"
        "| `cache_data` | Resultados reproducibles desde args serializables (DataFrames, texto, blobs pequeños). |\n"
        "| `cache_resource` | Handles globales pesados por proceso Worker (motor SQL, modelo, cliente).\n\n"
        "Ejecutá **`clear()` en el recurso/cache** cuando necesites refrescar después de escrituras."
    )

st.divider()
st.markdown(
    '<p class="seed-muted"><strong>ECS/Docker:</strong> la imagen arranca '
    "`streamlit run` en `0.0.0.0:8501`. Mantener health checks desde el Target Group ALB si aplica.",
    unsafe_allow_html=True,
)
