# Flujo spec-driven lite (sin CLI externa)

Mini-proceso inspirado en la idea de [GitHub spec-kit](https://github.com/github/spec-kit), adaptado a este repositorio **sin** instalar Specify ni slash-commands.

## Cuándo usarlo

- Cambios que tocan **varias páginas**, **nuevas dependencias**, **Docker/CI** o decisiones de diseño difíciles de revertir.
- Features que el usuario quiera documentar explícitamente antes de implementar.

## Pasos

### 1. Entender el objetivo

Leé [AGENTS.md](../../AGENTS.md) y el mapa [map.md](../map.md). Confirmá si el cambio toca archivos “infra del seed”.

### 2. Especificación breve (SPEC)

Creá (o pedí al usuario que cree) `specs/<nnn>-<slug>/SPEC.md` siguiendo la plantilla [../templates/feature-spec.template.md](../templates/feature-spec.template.md).

Incluí contexto, alcance, criterios de aceptación y **archivos que anticipás tocar**.

### 3. Plan de implementación (PLAN)

En el mismo directorio, `PLAN.md` con:

- Orden de cambios (dependencias → Docker → código → docs).
- Riesgos (por ejemplo, bump de Streamlit o cambio de entrypoint).
- Qué validar manualmente (comandos `streamlit run`, `docker build` si aplica).

### 4. Desglose de tareas (TASKS)

`TASKS.md` en checklist breve: ítems atómicos verificables (por ejemplo “añadir página `03_foo.py`”, “actualizar `configure_page` meta”, “documentar en README”).

### 5. Implementar y verificar

- Respetá siempre `configure_page` primero en cada script de página.
- Corré la app localmente según [README.md](../../README.md).
- Si el cambio afecta contenedor, validá build de imagen cuando el entorno lo permita.

## Relación con AGENTS.md

Este flujo **organiza el trabajo**; las reglas vinculantes siguen en [AGENTS.md](../../AGENTS.md). Si un SPEC contradice AGENTS, **ganan las reglas de AGENTS** salvo acuerdo explícito del humano dueño del repo.
