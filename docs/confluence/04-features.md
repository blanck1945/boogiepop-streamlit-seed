---
confluence_hint: página "Features and scope"
---

# Funciones y alcance del seed

| Área | Qué incluye |
|------|-------------|
| Multipágina | Patrón `app/pages/NN_*.py` con orden en sidebar. |
| Branding | `configure_page`: título de pestaña, icono (emoji o PNG), meta best-effort, CSS global del seed. |
| Demos | Página de estado de sesión y cachés; página in-app "Sobre el seed". |
| Documentación para agentes | `AGENTS.md`, carpeta `spec-kit/`, convención opcional `specs/`. |
| Contenedor y cloud | `Dockerfile`; ejemplo GitHub Actions ECR; jobs GitLab de guardas y flujo de ramas. |
| Protección de infra | `scripts/check_protected_paths.py` + manifest + `merge_request_branch_flow`. |

## Extensiones esperadas por el equipo producto

Autenticación delante del servicio, conexiones a APIs internas, almacenes de datos y jobs de datos quedan fuera del alcance mínimo de la plantilla; documentar cada extensión en Confluence como subpáginas de producto.
