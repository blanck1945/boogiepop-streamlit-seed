# Imagen reproducible para ECS/Fargate: escucha en 0.0.0.0:8501
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 streamlit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER streamlit

EXPOSE 8501

# Con STREAMLIT_SERVER_BASE_URL_PATH (ECS/ALB) el health vive bajo /{path}/_stcore/health.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os, urllib.request; p=(os.environ.get('STREAMLIT_SERVER_BASE_URL_PATH') or '').strip().strip('/'); path=f'/{p}/_stcore/health' if p else '/_stcore/health'; urllib.request.urlopen(f'http://127.0.0.1:8501{path}')"

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
