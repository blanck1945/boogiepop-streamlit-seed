---
confluence_hint: página "Deployment runbook"
---

# Runbook de despliegue (ejecutivo)

Detalle de comandos ampliado: ver **`README.md`** del repositorio (Docker, ECR, ECS).

## Build local de imagen

```bash
docker build -t boogiepop-streamlit-seed:local .
docker run --rm -p 8501:8501 boogiepop-streamlit-seed:local
```

## ECR y ECS (resumen)

1. Autenticación en el registry ECR de la cuenta/región.
2. Tag y push de la imagen con versión (SHA o semver).
3. Actualizar servicio ECS (`update-service --force-new-deployment`) o revisión de task definition según práctica IaC del equipo.

Registrar en Confluence los **valores reales** de cluster, servicio, ALB y cuentas cuando el proyecto esté provisionado.
