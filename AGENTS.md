# Guía para agentes y desarrolladores (Boogiepop Streamlit Seed)

Este archivo es la fuente humana/agente sobre **qué ofrece el seed**, **cómo extenderlo**, y **qué rutas están reservadas a infra**. En el futuro se añadirán *guards* automáticos; mantener este documento alineado reduce fricción.

Los LLMs/agentes encuentran también un **manual de entrada y onboarding** ordenado en [spec-kit/README.md](spec-kit/README.md): mapa rápido, stack, workflow spec-driven-lite y plantillas. **Aquí están las políticas contractuales**; `spec-kit` complementa con navegación y pasos opcionales.

## Propósito

Repositorio *seed* Streamlit multitarea listo para contenedores (**Docker → ECR → ECS**), con tema base, ejemplo de páginas, helpers de CSS, patrón de `session_state`, `cache_data` / `cache_resource` y workflows de ejemplo.

## Inventario rápido

| Ruta | Rol |
|------|-----|
| [app/Home.py](app/Home.py) | Punto de entrada multipágina (`streamlit run Home.py` dentro de `app/`). Landing y navegación. |
| [app/pages/](app/pages/) | Páginas secundarias. Convención: `NN_Título_snake_case.py`; `NN` controla orden en la sidebar. |
| [app/.streamlit/config.toml](app/.streamlit/config.toml) | Tema y servidor headless recomendados para Docker. |
| [app/styles/base.css](app/styles/base.css) | Estilos con prefijo `.seed-*` (alcance acotado). |
| [app/seed_main.py](app/seed_main.py) | Bootstrap de plataforma: `configure_page(...)` (primer `st.*` de cada script) con título/pestaña, icono, meta (best effort) y CSS global del seed. |
| [app/seed_ui.py](app/seed_ui.py) | Utilidades UI del seed (`inject_base_css`, `hero_card`). |
| [`maintainers/`](maintainers/README.md), [`scripts/check_protected_paths.py`](scripts/check_protected_paths.py) | Manifest de infra protegida + script compartido GitLab/`pre-commit` (ver [.gitlab-ci.yml](.gitlab-ci.yml)). |
| [requirements.txt](requirements.txt) | Dependencias **pinned** reproducibles para CI/Docker. |
| [Dockerfile](Dockerfile) | Runtime Python 3.12-slim + Streamlit binding `0.0.0.0:8501` + HEALTHCHECK `/_stcore/health`. |
| [.dockerignore](.dockerignore) | Artefactos excluidos del contexto Docker. |
| [.github/workflows/docker-ecr.yml](.github/workflows/docker-ecr.yml) | Plantilla OIDC AWS (build → ECR push → ECS opcional). |
| [README.md](README.md) | Uso humano local, freeze, Docker, ECR y ECS.

## Convenciones al implementar código

1. **`configure_page` primero**: cada `Home.py`/`pages/*.py` debe comenzar llamando `configure_page(...)` importada de `seed_main` **antes que cualquier otro `st.*`**, salvo comentarios/importaciones. Allí ajustás meta y el título/navegador.
2. **Nuevas pantallas**: añadí un archivo nuevo bajo `app/pages/` siguiendo el prefijo numérico. Evitá lógica de negocio duplicada: extraé funciones/utilidades fuera del script de página cuando crezcan.
3. **Estados de UI por usuario**: preferí `st.session_state`; usá prefijos coherentes (`feature_*`) para minimizar choques globales entre páginas.
4. **Caché**:
   - `@st.cache_data` para valores serializables idempotentes (lecturas reproducibles desde argumentos).
   - `@st.cache_resource` para handles por proceso Worker (motores externos, sesiones cliente largas).
5. **Personalización visual**: modificá antes el tema (`config.toml`); sólo recurriendo al CSS `.seed-*` expuesto cuando el tema no alcance. El CSS global ya se engancha mediante `configure_page`.

## Áreas modificables sin drama

- `app/pages/**` nuevos o modificados para la característica solicitada.
- Contenidos de bienvenida/marketing dentro de `app/Home.py` **siempre que** no cambies el contrato Docker (ver abajo).
- Pasar argumentos diferentes a **`configure_page(...)`** dentro de tus páginas para ajustar título/descripciones/meta (no requiere editar `seed_main.py`).
- `app/styles/base.css`, **siempre** usando clases/limitadores `.seed-*` y coordinando cargas mediante `configure_page` / helpers del seed (`seed_ui`).

## Tocá con cautela

- **`requirements.txt`**: cada cambio redefine el ambiente reproducible — actualizá con `pip freeze`/proceso del README y mencioná en la descripción PR qué librerías nuevas llegan transitivamente.
- **`Dockerfile`**: cambiar versión Python, comando `streamlit`, puerto u otro HEALTHCHECK tiene impacto en ECS/ALB y task definitions existentes — coordinación con infra.
- **`.github/workflows/docker-ecr.yml`**: placeholders de cuenta/rol; modificaciones erróneas rompen pipelines o seguridad IAM.

## No modificar sin consenso explícito (“infra del seed”)

Situaciones típicas de bloque (hasta tener policy formal):

- Eliminar **`HEALTHCHECK`**, mover **puerto/host** del `CMD` `streamlit` (debe mantener **`0.0.0.0:8501`** compatibles ECS salvo nueva convención de equipo).
- Renombrar `/app/Home.py`, moviendo el entrypoint esperado por CI/Docker/README sin actualizar todas las citas coherentes.
- Editar **`app/seed_main.py`** sólo mediante PR coordinado — contiene valores de plataforma y el orden garantizado (`set_page_config` → meta/CSS).

## PEP 8 y Streamlit práctico

- Funciones cortas por widget grueso donde sea posible; evitá lógico pesado dentro de bloques repetidos cada rerun sin `cache`/memo.
- Imports agrupados: stdlib, terceros, locales relativos cuando exista paquete.
- Preferí texto en Markdown claro ante HTML crudo cuando no necesité estilos del seed.

## Guards de infra (implementados)

**Fuente de verdad:** [`maintainers/seed-protected-paths.txt`](maintainers/seed-protected-paths.txt) más detalle operativo [`maintainers/README.md`](maintainers/README.md).

Se cruza cualquier archivo modificado (MR / push en CI GitLab mediante [`.gitlab-ci.yml`](.gitlab-ci.yml); opcionalmente `pre-commit` local) contra esa lista usando [`scripts/check_protected_paths.py`](scripts/check_protected_paths.py). Los bypass documentados están en [`README.md`](README.md).

**Ideas opcionales aún pendientes:**

- Lint en CI que inspeccione `CMD`/`HEALTHCHECK` del Dockerfile textualmente.
- Revisión de workflow GitHub/GitLab en busca de secretos texto plano.
- Lint de [`requirements.txt`](requirements.txt) para detectar líneas sin `==` pinning.

## Checklist rápido antes de abrir cambio grande

- [ ] ¿Cada página arranca con `configure_page(...)` antes de otros `st.*`?
- [ ] ¿Hay datos cacheables reproducibles vs recursos singleton? → elijo `cache_data` vs `cache_resource`.
- [ ] ¿El cambio tocó infra? coordiné Dockerfile/workflow/requirements antes de fusionar.

Si algo no está claro, tratá **`AGENTS.md` + esta lista** como la fuente de verdad inicial hasta que lleguen automatismos formales.
