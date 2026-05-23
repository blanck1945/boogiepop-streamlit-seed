---
title: Guía de anatomía del spec-kit (uso en otros seeds, p. ej. React)
tipo: solo-documentacion
uso: desarrollo-equipo-multi-seed
no_es_artifact_deploy: true
---

# Guía: cómo está armado este spec-kit (replicarlo en otros seeds)

Este archivo es **solo documentación metodológica**. No forma parte del runtime Streamlit ni de lo que deployás como app. Sirve para describir una **forma portable** de documentar trabajo con agentes y LLMs, de modo que otros seeds (por ejemplo uno de React) puedan **copiar o adaptar** la misma estructura cambiando principalmente rutas y notas del stack.

> Si querés usarlo sólo como memo local entre equipos sin versionarlo, podés moverlo fuera del repo o añadirlo a `.gitignore`. Si lo querés como **contrato vivo** entre varios seeds paralelos (`streamlit-seed`, `react-seed`), conviene tenerlo dentro del árbol y mantenerlo al día.

## Anatomía actual (este repositorio)

```text
.
├── AGENTS.md                        # Contrato técnico: qué sí / qué no / convenciones (fuente de verdad)
├── README.md                        # Ejecución local, deps, Docker, CI (humano)
├── spec-kit/
│   ├── README.md                   # Índice + orden de lectura recomendado al agente
│   ├── map.md                      # Mapa rápido por tipo de ruta (“producto vs infra vs docs solamente”)
│   ├── stack.md                    # Herramientas + versionado + cómo corre el seed
│   ├── streamlit-notes.md          # Peculiaridades del stack Streamlit de este proyecto
│   ├── workflows/
│   │   └── spec-driven-lite.md     # Workflow opcional tipo spec → plan → tasks (sin CLI externa)
│   └── templates/
│       └── feature-spec.template.md
└── specs/                           # Opcional: features numeradas SPEC/PLAN/TASKS
    └── README.md
```

Ideas invariantes tras clonar esta estructura en otro proyecto:

| Concepto | Rol |
|-----------|-----|
| `AGENTS.md` en raíz | Normas ejecutables (“no tocar X”, “primer paso obligatorio Y”). |
| `spec-kit/` | Manual principal de entrada para agentes/humanos al codear sobre el seed. |
| `spec-kit/README.md` | Orden de lectura antes de editar código. |
| `spec-kit/workflows/` | Procesos largos opcionales. |
| `spec-kit/templates/` | Plantillas reutilizables sin tooling adicional. |
| `spec-kit/<stack>-notes.md` | Peculiaridades del stack (acá Streamlit). En React sería algo como `vite-react-notes.md`. |
| `specs/` | Trazabilidad por carpeta `-nnn_slug` cuando hace falta. |

### Qué queda necesariamente específico del stack aquí

- [`streamlit-notes.md`](streamlit-notes.md): `configure_page`, `seed_main.py`, carpeta [`app/pages/`](../app/pages/), estado y caché de Streamlit.  
En un seed React estos temas equivalen de otro modo: router, layout raíz, providers, tema, meta (Helmet/remix-handle/Next metadata), estilos globales, ESLint/Vite/Webpack.

## Mapeo sugerido: Streamlit Seed → Seed React típico

Analogía habitual (ajústalo a tu plantilla React concreta):

| Esta seed (Python/Streamlit) | Analogía habitual (React/Vite u otro bundler) |
|------------------------------|-----------------------------------------------|
| [`app/Home.py`](../app/Home.py), [`app/pages/`](../app/pages/) | `src/App.tsx`, `src/pages/` o rutas declaradas (`routes/`). |
| [`app/seed_main.py`](../app/seed_main.py), `configure_page` | punto de entrada cliente (`main.tsx`), providers, tema, meta-document head. |
| [`app/styles/base.css`](../app/styles/base.css) | `global.css`, Tailwind/theme, tokens CSS. |
| [`requirements.txt`](../requirements.txt), [`Dockerfile`](../Dockerfile) | `package.json` + lockfile, `Dockerfile` multi-stage específico de Node/build estático/servidor. |
| Demo en [`app/pages/01_Demo_estado_y_cache.py`](../app/pages/01_Demo_estado_y_cache.py) | Página/playground sólo desarrollo opcional detrás de flag. |

En `map.md` del seed React vas a querer rutas modificables día a día (`src/features/...`), infra de build (`vite.config.ts`, pipelines), y artefactos de plataforma “no tocables sin consenso”.

## Lista mínima al replicar (checklist)

1. Copiar `spec-kit/` y `specs/README.md`.
2. Sustituir o renombrar `streamlit-notes.md` por notas propias del stack destino (React/Vite/etc.).
3. Actualizar rutas en `map.md` y comandos/stack en `stack.md`.
4. Revisar `workflows/spec-driven-lite.md`: sólo ajustes donde aparecen comandos locales (por ejemplo Streamlit ⇄ `pnpm dev`).
5. Escribir o adaptar **`AGENTS.md`** del nuevo repo si aún no existe (las reglas vinculantes siguen ahí).

## Relación con el spec-kit oficial de GitHub

Esta carpeta adopte sólo la **filosofía** (Markdown, fases, carpetas opcionales). La CLI y los comandos tipo `/speckit-*` de [github/spec-kit](https://github.com/github/spec-kit) son opcionales y no están integrados aquí.

## Mantener varios seeds alineados

Compará de vez en cuando:

| Artefacto | Objetivo alineación |
|-----------|---------------------|
| `AGENTS.md` | Misma filosofía zonas modificables vs infra. |
| `spec-kit/workflows/spec-driven-lite.md` | Puede compartirse casi igual entre repos. |
| `templates/feature-spec.template.md` | Diverge sólo donde el stack cambia (rutas, chequeos QA). |

Plantilla de política “no tocar archivos de plataforma” + CI/GitLab: **[proteccion-usuario-vs-plataforma-react.md](proteccion-usuario-vs-plataforma-react.md)**.

Eso ayuda cuando el mismo operador salta entre Streamlit y React sin releer convenciones distintas desde cero.
