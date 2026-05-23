# Streamlit para este repo (agente)

## Primer comando en cada página

Por convención de este seed, **la primera función Streamlit ejecutada debe ser** `configure_page(...)` desde [app/seed_main.py](../app/seed_main.py). No insertes otros `st.*` antes sin una razón muy fuerte (rompe garantías multi-página/meta/CSS).

Consultá también la guía UI in-app **[app/pages/02_Sobre_el_seed.py](../app/pages/02_Sobre_el_seed.py)**.

## Multipágina

Los scripts bajo [app/pages/](../app/pages/) forman la navegación lateral automática. Usá el prefijo numérico `NN_` en el nombre de archivo para controlar el orden.

## Estado y caché

- **`st.session_state`**: persistencia por sesión de usuario en el navegador mientras el servidor permanece coherente.
- **`@st.cache_data` / `@st.cache_resource`**: según guía en [AGENTS.md](../AGENTS.md) y demo en [app/pages/01_Demo_estado_y_cache.py](../app/pages/01_Demo_estado_y_cache.py).

## CSS global

- Colores base: [app/.streamlit/config.toml](../app/.streamlit/config.toml).
- Estilos adicionales prefijados `.seed-*`: [app/styles/base.css](../app/styles/base.css).
- **`configure_page`** dispara también la inyección del CSS mediante [app/seed_ui.py](../app/seed_ui.py) (una vez por sesión con el guard interno del seed).

## Meta tags y pestaña del navegador

`título`/favicon soportados vía **`st.set_page_config`** se delegan dentro de **`configure_page`**.

Las etiquetas `<meta>` extras generadas en Python son **best effort** dentro del árbol de la app Streamlit; **no** equivalen a parchear el `<head>` estático del `index.html` del paquete Streamlit. Para SEO/open graph “duro” en entornos productivos, lo habitual es un paso de build en la imagen — documentado en el docstring de [app/seed_main.py](../app/seed_main.py).
