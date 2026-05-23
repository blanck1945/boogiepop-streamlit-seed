# Mapa rápido de rutas (agente)

Referencia breve. Las reglas detalladas viven en [AGENTS.md](../AGENTS.md).

## Modificá con frecuencia (producto / features)

| Ruta | Cuándo |
|------|--------|
| [app/Home.py](../app/Home.py) | Landing, copy, enlaces a páginas. |
| [app/pages/](../app/pages/) | Nuevas pantallas; `NN_Nombre.py` controla el orden en la barra lateral. |
| [app/styles/base.css](../app/styles/base.css) | Estilos `.seed-*` compartidos (evitá hackear el DOM interno de Streamlit). |

## Ajustás con conocimiento explícito (afectan muchas áreas)

| Ruta | Cuándo |
|------|--------|
| [requirements.txt](../requirements.txt) | Nuevas librerías o bump de deps; siempre revisar reproducibilidad pinned. |
| [README.md](../README.md) | Comandos, flujo local, Docker publicado. |

## Infra del seed — coordinar con equipo / sólo PR de plataforma

| Ruta | Motivo |
|------|--------|
| [app/seed_main.py](../app/seed_main.py) | Orden garantizado (`configure_page`: `set_page_config` → CSS/meta globales del seed). |
| [Dockerfile](../Dockerfile) | Python base, comando `streamlit`, puerto/host, HEALTHCHECK ECS. |
| [.github/workflows/docker-ecr.yml](../.github/workflows/docker-ecr.yml) | CI push ECR / ECS opcional. |
| [app/.streamlit/config.toml](../app/.streamlit/config.toml) | Tema y defaults de servidor recomendados en contenedor. |
| [maintainers/](../maintainers/README.md), [`.gitlab-ci.yml`](../.gitlab-ci.yml), [`.gitlab/CODEOWNERS`](../.gitlab/CODEOWNERS) | Infra declarada cubierta por guard manifest + approvals pipeline (GitLab); ver [README § Protección](../README.md). |
| [`scripts/check_protected_paths.py`](../scripts/check_protected_paths.py) | Chequeo compartido CI / `pre-commit` local. |

## Documentación sólo Markdown (sin impacto runtime)

| Ruta |
|------|
| [AGENTS.md](../AGENTS.md) |
| [spec-kit/README.md](README.md) | Índice para agentes; enlaza orden de lectura y plantillas. |
| [specs/](../specs/README.md) (convención de features) |
