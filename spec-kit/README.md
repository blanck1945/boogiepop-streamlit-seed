# Spec-kit ligero para agentes (Boogiepop Streamlit Seed)

Esta carpeta **no sustituye** las reglas técnicas del repositorio. Es un punto de entrada y un **manual de rutas/flujos** para LLMs que implementan cambios sobre este seed.

Este “spec-kit” **no** usa la CLI oficial de [GitHub spec-kit](https://github.com/github/spec-kit) ni comandos tipo `/speckit-*`. Son sólo Markdown y una convención opcional para **specs/features** enumeradas.

## Orden de lectura recomendado (agente)

1. **[AGENTS.md](../AGENTS.md)** — contrato: qué tocar, qué no y convenciones de código (**obligatorio**).
2. **[map.md](map.md)** — mapa rápido por tipo de archivo.
3. **[stack.md](stack.md)** — runtime, Docker y versiones efectivas del seed.
4. **[streamlit-notes.md](streamlit-notes.md)** — detalles mínimos de Streamlit/multipágina/meta/CSS.
5. **[workflows/spec-driven-lite.md](workflows/spec-driven-lite.md)** — flujo opcional tipo spec → plan → tareas antes de codificar grandes cambios.
6. Carpeta opcional **`../specs/`** — véase su [README](../specs/README.md) para ubicar SPEC/PLAN/TASKS por feature.

## Plantillas

- Feature / especificación inicial: **[templates/feature-spec.template.md](templates/feature-spec.template.md)** (copiá a `specs/<nnn>-<slug>/SPEC.md` si usás ese flujo).

## Replicar en otros seeds (p. ej. React)

Documentación solo metodológica: **[guia-replicacion-react-y-otros.md](guia-replicacion-react-y-otros.md)** describe la anatomía de esta carpeta y un mapeo sugerido a un proyecto React/Vite equivalente.

Protección de archivos de plataforma + CI (portable): **[proteccion-usuario-vs-plataforma-react.md](proteccion-usuario-vs-plataforma-react.md)** — qué no debería tocar el usuario final, manifest, tres capas y checklist para el seed React.

## Reglas prácticas para el agente

- **Ejecutá comandos de terminal, git, pushes o herramientas externas sólo cuando el usuario lo pida**, salvo automatización ya acordada en el propio proyecto.
- **No dupliques** tablas grandes de política: enlazalas desde [AGENTS.md](../AGENTS.md).
- Mantené el entrypoint **`streamlit run Home.py` desde la carpeta [app/](../app/)**, salvo refactor coordinado que actualice Dockerfile y documentación junto.
