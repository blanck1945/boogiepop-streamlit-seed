---
confluence_hint: página "Resumen" o descripción corta para stakeholders
related_repo_paths: /
---

# Overview — Boogiepop Streamlit Seed

## Qué es

**Boogiepop Streamlit Seed** es una plantilla de aplicación **Streamlit multipágina** pensada como punto de partida para equipos que quieren dashboards internos reproducibles en **Docker**, publicación opcional por **AWS ECR** / **ECS** y documentación ordenada para **desarrollo asistido** (agentes, guías tipo spec-kit).

## Para quién

| Audiencia | Uso típico |
|-----------|------------|
| **Desarrollo producto** | Añadir pantallas en `app/pages`, extender contenido UI en `app/Home.py`. |
| **Plataforma / DevOps** | Mantener Dockerfile, CI GitLab, manifest de infra protegida, releases taggeados hacia producción. |
| **Gestión / seguridad** | Entender alcance técnico, flujo de ramas y qué archivo es infra de plataforma vs trabajo diario de feature. |

## Limitaciones conscientes del seed

- No es SaaS multitenant cerrado ni auth incorporada más allá de lo que añada el equipo en su entorno.
- Metadatos OpenGraph desde Python son mejora parcial en SPA; previews sociales pueden requerir parche Docker del `index.html` de Streamlit (documentado en `app/seed_main.py`).

## Enlaces rápidos (repo fuente)

- Uso habitual local: `README.md` en la raíz del repositorio.
- Políticas y rutas modificables vs protegidas: `AGENTS.md`.
- Ramas vivas CI: `docs/gitlab-branching.md`.
