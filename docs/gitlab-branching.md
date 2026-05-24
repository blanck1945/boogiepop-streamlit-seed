# Flujo GitLab (develop · staging · main)

Tres ramas de largo plazo: **`develop`**, **`staging`**, **`main`**. Parte de la política vive en configuración del proyecto GitLab (ramas protegidas); esta documentación y [`.gitlab-ci.yml`](../.gitlab-ci.yml) refuerzan merges correctos mediante CI.

## Qué hace CI en este repo

| Job | Función |
|-----|---------|
| **`protect_seed_manifest`** | Correlaciona rutas modificadas contra [`maintainers/seed-protected-paths.txt`](../maintainers/seed-protected-paths.txt). |
| **`merge_request_branch_flow`** | Ejecuta [`scripts/gitlab/validate_mr_branch_flow.sh`](../scripts/gitlab/validate_mr_branch_flow.sh) solo en pipelines de MR. |

Habilitá en GitLab *Settings → Merge requests → Merge request pipelines*.

## Flujo esperado entre ramas

Sólo se validan **merge requests**.

| MR hacia... | Permitido desde... |
|-------------|--------------------|
| `develop` | `feature/*`, `feat/*`, `fix/*`, `docs/*`, `chore/*`, `hotfix/*`, bots `renovate/*`, `dependabot*` |
| `staging` | sólo **`develop`** |
| `main` | **ningún MR** — el pipeline fallará. Promové producción mediante **tag**/job de release desde la línea de `staging`. |

Bypass emergencias: variable **`BRANCH_FLOW_BYPASS=1`** (masked) o etiqueta **`branch-flow-bypass`**.

## Producción desde `staging` mediante tag

CI no crea merges automáticamente contra `main` sin secreto/token de release. Opciones típicas:

1. Tag anotado `vX.Y.Z` sobre commit aprobado de `staging` + job posterior (añadís más adelante) que FF-mergee a `main` con token proyecto.
2. Proceso humano: después del tag permitís temporalmente MR `staging→main` y relajás el script (consultá al equipo infra antes).

## Ramos protegidas (GitLab UI)

Orientación habitual:

| Rama | Push usuarios |
|------|---------------|
| `develop`, `staging`, `main` | Desactivado merge/push irregular; merges cuando pipeline verde. |

Opcionalmente hacés **`develop`** la default branch si el equipo trabaja día a día allí.

## Crear líneas estable por primera vez

````bash
git fetch origin
git checkout -b develop origin/main || git checkout -b develop
# ... o desde commit plantilla ...
git push -u origin develop
git checkout -b staging develop
git push -u origin staging
````

Alinear `main` con release actual según proceso.
