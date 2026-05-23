# Boogiepop Streamlit Seed

Plantilla lista para desarrolladores: app multipágina Streamlit con **dependencias congeladas**, **Docker**, guía para **AWS ECR** y **ECS**, y **`AGENTS.md`** para automatizar trabajo con herramientas de IA sin romper infraestructura.

## Ejecutar en local

1. Creá un entorno virtual e instalá las dependencias (siempre desde la raíz del repo):

```bash
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt   # PowerShell / Windows
# source .venv/bin/activate && pip install -r requirements.txt   # macOS/Linux
```

2. Levantá la app **desde el directorio `app/`**, para que `pages/` y `.streamlit/config.toml` se resuelvan como espera Streamlit:

```bash
cd app
streamlit run Home.py
```

3. Abrí el navegador en la URL indicada por la consola (por defecto `http://localhost:8501`).

## Actualizar dependencias (freeze)

Este repo lleva todas las líneas **pinned** (`paquete==versión`). Para aplicar cambios compatibles manteniendo la idea de “solo `requirements.txt`”:

```bash
.\.venv\Scripts\pip install -U streamlit           # ejemplo
.\.venv\Scripts\pip freeze > requirements.tmp
# opcional: filtrá pip/setuptools/editables y reemplazá requirements.txt manualmente con el nuevo freeze
mv requirements.tmp requirements.txt
```

Recomendación: ejecutá la instalación y el `freeze` **desde el mismo Python y SO** que usará la imagen Docker (o directamente construí la imagen y validá allí) para evitar sorpresas con wheels binarios.

## Docker (local y ECS-ready)

Desde la raíz del repositorio:

```bash
docker build -t boogiepop-streamlit-seed:local .
docker run --rm -p 8501:8501 boogiepop-streamlit-seed:local
```

La imagen escucha en `0.0.0.0:8501` y expone `HEALTHCHECK` contra `/_stcore/health` (útil en ECS con health checks similares o checks del ALB).

## Publicar en Amazon ECR

1. Creá un repositorio ECR en la cuenta y región deseadas.
2. Autenticate con `aws ecr get-login-password` y `docker login` al registry (ver [documentación oficial de ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-docker-image.html)).
3. Etiquetá y subí la imagen:

```bash
AWS_ACCOUNT_ID=123456789012
AWS_REGION=us-east-1
REPO=boogiepop-streamlit-seed
TAG=$(git rev-parse --short HEAD)

docker tag boogiepop-streamlit-seed:local ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO}:${TAG}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO}:${TAG}
```

## Desplegar en Amazon ECS

1. Definí una **task definition** (Fargate o EC2) cuyo contenedor use la imagen que acabás de subir.
2. Asociá un **servicio** al cluster con la task definition activa.
3. Tras cada push de imagen (nuevo digest o tag), forzá un rollout:

```bash
aws ecs update-service \
  --cluster mi-cluster \
  --service mi-servicio-streamlit \
  --force-new-deployment
```

Si cambiás el **digest** preservando `:latest`, `force-new-deployment` basta cuando el task definition usa `:latest`; si etiquetás por SHA, también podés crear una nueva revisión de task definition que apunte ese tag.

Hay una plantilla de **GitHub Actions** en [.github/workflows/docker-ecr.yml](.github/workflows/docker-ecr.yml) configurada para OIDC a AWS, push a ECR y un paso opcional de ECS.

Variables sugeridas (GitHub Actions → Variables): `AWS_REGION`, `ECR_REPOSITORY`, opcionalmente `ECS_CLUSTER_NAME` y `ECS_SERVICE_NAME`. Secreto: `AWS_ROLE_TO_ASSUME` (ARN del rol IAM con permisos de ECR/ECS necesarios).

## Protección de rutas infra (GitLab)

Tres capas complementarias (**ninguna sustituye rama protegida + MR + revisión humana útil como fuerte**):

| Capa | Qué es | Implementación aquí |
|------|--------|---------------------|
| **Commit local** (best-effort) | Reduce cambios accidentales en artefactos de plataforma | Hook opcional **`pre-commit`**: ejecutá `pip install pre-commit` y **`pre-commit install`** en la raíz del repo (`[.pre-commit-config.yaml](.pre-commit-config.yaml)`). Bypass temporal sólo mantenedores: variable de entorno **`SEED_GUARD_BYPASS=1`** (spoofeable por diseño). |
| **Push / MR (GitLab)** | Evita merges sin approvals sobre infra | **`[.gitlab/CODEOWNERS](.gitlab/CODEOWNERS)`** como plantilla: descomentá rutas + `@grupo`; activá approvals en proyecto. Rama default sin push directo + push rules opcionales (email corporativo ayuda sólo ante errores, no garantiza identidad fuerte sin firmado). |
| **Pipeline** | Falla MR que toque infra sin bypass coordinado | Job **`protect_seed_manifest`** en **[`.gitlab-ci.yml`](.gitlab-ci.yml)** corre `scripts/check_protected_paths.py` contra **`maintainers/seed-protected-paths.txt`**. Bypass controlado: etiqueta **`seed-infra-approved`** en el MR (`CI_MERGE_REQUEST_LABELS`) o **`SEED_INFRA_CI_FLAG=1`** sólo mediante variable masked+protected de GitLab definida por plataforma. Alternativa opcional pareja **`SEED_INFRA_CI_BYPASS_TOKEN` / `SEED_INFRA_CI_BYPASS_EXPECTED`** idénticas (masked). Variación `GIT_DEPTH: "0"` evita merges shallow rotos sobre `merge-base`. |

Lista exacta de globs protegidos y filosofía del manifest: **`[maintainers/README.md](maintainers/README.md)`**. La **GitHub Action** ejemplo en [.github/workflows/docker-ecr.yml](.github/workflows/docker-ecr.yml) sigue en el mismo manifest de protección; si migrás sólo GitLab mantenelo coherente o elimina esas líneas conscientemente desde un MR infra.

## Documentación orientada a agentes

Lee [AGENTS.md](AGENTS.md) para conocer inventario del seed, zonas modificables vs “no tocar” y convenciones de código antes de refactorizar automatizado.

Para onboarding paso a paso dirigido a LLMs —mapa rápido, stack, plantillas opcionales y flujo spec-driven-lite— revisá también [spec-kit/README.md](spec-kit/README.md) y la convención de carpetas opcionales [specs/README.md](specs/README.md).

## Contenidos del seed en la UI

La app incluye páginas de ejemplo y una guía in-app (**Sobre el seed**) sobre CSS base, tema, multipágina (`pages/`), `st.session_state` y decorators de caché.
