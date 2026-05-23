# Archivos fuera del alcance habitual del usuario y cómo están protegidos (guía portable para otros seeds)

Documento pensado para **equipos que montan otros seeds** (por ejemplo uno en **React**): describe qué clase de archivo declaramos como **infra/plataforma**, cómo se versiona esa lista en un solo archivo y cómo aplicamos tres capas (local opcional → GitLab MR/ownership → pipeline). El proyecto de referencia concreto en el que vivió primero esta política es el **Boogiepop Streamlit Seed**.

## Alcance de expectativas (importante)

- **Usuario del seed**: quién clona la plantilla y construye su producto (páginas, features).
- **Mantenedor de plataforma**: equipo que evoluciona el esqueleto (Docker base, entrada de app, manifests de dependencias duras).

**El hook local (`pre-commit`) y whitelist por `user.email`** son útiles sólo contra errores innocentes / guía rápida. **No** son controles anticopia ni anticuentas compartidas: cualquiera con el repo puede forzar refs o ignorar hooks con flags expuestos. La garantía práctica está en GitLab (**MR obligatorio**, **pipeline rojo**, **CODEOWNERS/approvals**).

## Lista única fuente de verdad (manifest)

Modelo reproducible:

1. Un archivo texto con **glob patterns** posix (unas líneas, comentarios con `#`).
2. Un único programa (script) que cruza rutas modificadas contra el manifest para **stdin** (_hook_) o **dif entre dos SHAs** (_CI_).

En este repositorio:

| Artefacto | Path |
|-----------|------|
| Manifest | [`maintainers/seed-protected-paths.txt`](../maintainers/seed-protected-paths.txt) |
| Descripción corta mantenedores | [`maintainers/README.md`](../maintainers/README.md) |
| Checker | [`scripts/check_protected_paths.py`](../scripts/check_protected_paths.py) |
| Wrapper pre-commit | [`scripts/pre_commit_seed_guard_wrapper.py`](../scripts/pre_commit_seed_guard_wrapper.py) |
| GitLab CI | [`.gitlab-ci.yml`](../.gitlab-ci.yml) |
| Hooks declarados | [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) |

Contenido **actual** protegido (resumen conceptual; ver manifest para globs exactos):

- **`Dockerfile` / `.dockerignore`**: reproducibilidad de imagen.
- **`requirements.txt`**: deps **pinned**.
- **`app/seed_main.py`**: bootstrap garantizado (`configure_page` ordenado).
- **`app/.streamlit/config.toml`** y **`app/seed_ui.py`**: branding/tema/UI base coordinada por plataforma.
- **`maintainers/`**, **`scripts/check_protected_paths.py`** y variantes relacionadas **y** manifests **CI/GitHub/GitLab hooks**: evitar borrar chequeos inadvertidamente.
- **Workflows ejemplo** `.github/workflows/**`.

Zona habitual **sí modificable por quien adopte el seed** (aquí):

- **`app/Home.py`**, **`app/pages/**`** (screens), **`app/styles/base.css`** bajo convenciones (clases prefijadas), documentación Markdown de producto (`README` copy interno opcional tras acordar equipo).

Analogía rápida al portar React (orientativa, no cerrada):

| Streamlit Seed (este repo) | React seed típico |
|----------------------------|-------------------|
| `app/seed_main.py` (`configure_page`) | `src/main.tsx` + Providers raíz que fijan layout/theme/metadata |
| `app/.streamlit/config.toml` | tokens/tema Tailwind/CSS variables/`theme-provider` establecido por plataforma |
| `requirements.txt` | `package-lock`/`pnpm-lock` + política pinning explícito |
| `app/Home.py` + `pages/*` rutas públicas usuario | páginas bajo `src/pages` o rutas donde el usuario agrega vistas |
| `Dockerfile` + CI YAML | igual concepto |

## Las tres capas de protección (matriz reproducible)

| Capa | Qué hace | En este proyecto | Equivalente típico en React seed |
|------|----------|------------------|----------------------------------|
| **1. Commit local opcional** | Bloque *antes del commit staged* errores triviales tocando infra | Hook `pre-commit` que llama al checker contra `git diff --cached --name-only` | Igual herramienta `pre-commit` o script `pnpm lint:infra` lanzado husky |
| **2. Policies GitLab antes del merge** | Evita merges directos sobre default sin revisión infra | Rama protegida; plantilla [.gitlab/CODEOWNERS](../.gitlab/CODEOWNERS) (**descomenta owners reales antes de usar**); push rules opcionales (email empresa como filtro suave) | Idéntico en GitLab; alternativamente branch protection + required reviewers en GitHub |
| **3. Pipeline CI** | Falla el MR si el diff toca manifest sin bypass explícito | Job `protect_seed_manifest` en `.gitlab-ci.yml` compara base vs `CI_COMMIT_SHA` | Job stage `guard` que ejecuta el **mismo script** o TypeScript port del manifest |

### Bypasses coordinados (no “secretos mágicos” irrazonables)

Documentados en el checker y en [README § Protección de infra](../README.md):

- **Etiqueta MR** `seed-infra-approved` (variable `CI_MERGE_REQUEST_LABELS`).
- **Variable CI masked+protected** `SEED_INFRA_CI_FLAG=1` (recomendada frente a duplicar tokens largos).
- Alternativa espejo `SEED_INFRA_CI_BYPASS_TOKEN` / `SEED_INFRA_CI_BYPASS_EXPECTED` idénticos (masked).
- **Sólo desarrollo mantenedor local:** `SEED_GUARD_BYPASS=1` (equivale a “confío en mi laptop”, no a política en servidor).

En React seed copiá la **misma semántica** de nombres o renombrá consistentemente y documentá en `AGENTS.md` del nuevo repo.

## Pasos mínimos para implementarlo en un seed React

1. **Clonar la idea del manifest** → `maintainers/seed-protected-paths.txt` adaptado (rutas `vite.config.ts`, `src/platform/**`, `Dockerfile`, lockfile, `.gitlab-ci.yml`, etc.).
2. **Reutilizar o portar** `check_protected_paths.py` (Python OK en CI Node image con `python:3.x` sidecar, o reescribir 40 líneas en Node leyendo el mismo txt).
3. **Añadir job GitLab** equivalente a `protect_seed_manifest` con `GIT_DEPTH: "0"` si usás `merge-base`.
4. **CODEOWNERS** comentado hasta que exista `@grupo` real.
5. **Documentar** en `AGENTS.md` / README qué **no** toca el usuario y la matriz de capas (copiar sección del README de este repo).
6. **Pre-commit** opcional con `pass_filenames: false` + `always_run: true` si querés que corra en cada commit (latencia baja).

## Lecturas cruzadas

- Políticas humanas + agentes: [`AGENTS.md`](../AGENTS.md) (inventario y “Guards de infra”).
- Flujo general multi-seed: [`spec-kit/guia-replicacion-react-y-otros.md`](guia-replicacion-react-y-otros.md).
