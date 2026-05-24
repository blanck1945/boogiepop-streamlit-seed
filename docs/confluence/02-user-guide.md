---
confluence_hint: página "User guide"
---

# Guía de usuario (desarrollador que adopta el seed)

## Requisitos

- Python 3.11+ típico (la imagen Docker usa **3.12** para alinear con prod).
- Git y terminal según flujo de ramas del equipo.

## Puesta en marcho local

1. Clonar el repositorio.
2. Crear virtualenv e instalar dependencias **pinned**:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Ejecutar la app **desde la carpeta `app/`** (resuelve `pages/` y `.streamlit/config.toml`):

```bash
cd app
streamlit run Home.py
```

Por defecto: `http://localhost:8501`.

## Rutas conocidas

| Ruta en el repo | Rol |
|-----------------|-----|
| `app/Home.py` | Landing y navegación in-app. |
| `app/pages/NN_slug.py` | Páginas secundarias; `NN` ordena la barra lateral. |
| `app/seed_main.py` | Bootstrap de plataforma (`configure_page`); no es el lugar habitual de features. |
| `app/assets/seed.png` | Ejemplo de favicon por imagen (configurar `page_icon` en `configure_page`). |

En cada script de página, la **primera** llamada Streamlit debe ser `configure_page(...)` importada de `seed_main`.

## Hooks opcionales

`pre-commit install` (tras `pip install pre-commit`) ayuda a no commitear cambios accidentales en rutas de infra listadas en `maintainers/seed-protected-paths.txt`.

## Documentar nuevas features

Preferir nuevas entradas bajo `app/pages/`; para trabajo espec-driven opcional ver `specs/` y `spec-kit/`.
