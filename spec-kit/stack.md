# Stack del seed (referencia rápida)

Fuente técnica de verdad: [requirements.txt](../requirements.txt) y [Dockerfile](../Dockerfile). Si estos dos divergen, priorizá alinear Dockerfile con lo que declará frozen deps después de instalación en imagen.

## Python y Streamlit

- **Dockerfile**: imagen base `python:3.12-slim-bookworm` (ver archivo para detalles).
- **Streamlit y dependencias**: versiones enumeradas línea por línea en [requirements.txt](../requirements.txt) (formato pinned `paquete==versión`).
- Ejecución recomendada en desarrollo local: mismo entorno Python del README (venv con esas dependencias instaladas desde la raíz del repo).

## Entrypoint aplicación

- Código navegable vivo bajo **[app/](../app/)**.
- **Comando local**: dentro de `app/`, ejecutar `streamlit run Home.py` (véase [README.md](../README.md)).
- **Docker**: el `WORKDIR` de la imagen es `/app` con el contenido de `app/` copiado; el `CMD` ejecuta Streamlit contra `Home.py` en **0.0.0.0:8501** con headless recomendado (ver Dockerfile).

## Despliegue previsto en la plantilla

- Contenedor ECS/Fargate detrás de ALB habitual (health check HTTP `/_stcore/health` documentado junto al Dockerfile original del seed).
- Publicación imagen AWS ECR y workflow ejemplo en [.github/workflows/docker-ecr.yml](../.github/workflows/docker-ecr.yml).
