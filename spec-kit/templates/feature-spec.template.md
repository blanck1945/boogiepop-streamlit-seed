# SPEC: <título corto de la feature>

**ID sugerido de carpeta**: `specs/<nnn>-<slug>/` (por ejemplo `001-auth-sidebar`).

**Estado**: borrador | lista para implementar | cerrado

---

## Contexto

- Problema o oportunidad que resuelve.
- Usuario o flujo principal afectado.
- Decisiones ya tomadas por el equipo humano.

## Alcance dentro (in-scope)

- Lista concreta de comportamientos o pantallas nuevas/modificadas.

## Fuera de alcance (out-of-scope)

- Lo que explícitamente **no** haremos en esta iteración.

## Diseño esperado en UI (opcional)

- Wireframe textual / estados loading-empty-error si aplica.
- Preferencias de texto (idioma español si el proyecto lo mantiene).

## Archivos que probablemente tocaremos

Marca sólo anticipación inicial; revisá durante el PLAN.

| Ruta probable | Cambio esperado |
|---------------|-----------------|
| `app/pages/…` | |
| `app/Home.py` | |
| `app/seed_ui.py` / `app/styles/base.css` | |
| `requirements.txt` | |
| `Dockerfile` / `.github/workflows/…` | |

## Convenciones del seed que debemos respetar

- **`configure_page` primero** en cada script de página; ver código en [app/seed_main.py](../../app/seed_main.py).
- Multipágina: convención `NN_*.py`.
- Coordinar infra si se tocara [app/seed_main.py](../../app/seed_main.py), [Dockerfile](../../Dockerfile) u otro marcado como “infra” en [AGENTS.md](../../AGENTS.md).

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| | |

## Criterios de aceptación (checklist verificables)

- [ ]
- [ ]

## Referencias

- [AGENTS.md](../../AGENTS.md)
- Mapa rápido: [spec-kit/map.md](../map.md)
