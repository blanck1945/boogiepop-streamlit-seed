# GitLab CI/CD — Streamlit (`boogiepop-streamlit-seed`)

Patrón alineado con **`boogiepop-react-seed`** ([`docs/GITLAB-DEPLOY.md`](../../boogiepop-react-seed/docs/GITLAB-DEPLOY.md)) y el **host**.

## Flujo por rama

| Momento | Pipeline | Deploy |
|---------|----------|--------|
| **MR → `main`** | `protect_seed_manifest` + `merge_request_branch_flow` | — |
| **Push / merge a `main`** | **`docker-publish-streamlit-prod`** + **`deploy-streamlit-ecs-prod`** | **Automático** → ECR `:latest` + rollout ECS |
| **Push a `develop`** | guard + jobs **manual** | Staging opcional (`:develop`) |

## Variables (Settings → CI/CD → Variables)

Mismas credenciales AWS que el **host**:

| Variable | Valor / default |
|----------|-----------------|
| **`ECR_REGISTRY`** | Default en YAML: `653876198281.dkr.ecr.us-east-1.amazonaws.com` (override opcional) |
| **`AWS_ACCESS_KEY_ID`** / **`AWS_SECRET_ACCESS_KEY`** | **Obligatorias** — ECR push + ECS update (Protected en `main`) |
| **`STREAMLIT_ECR_REPOSITORY`** | Default YAML: `boogiepop-streamlit` |
| **`ECS_CLUSTER_NAME`** | Default: `boogiepop-api-cluster` |
| **`ECS_STREAMLIT_SERVICE_NAME`** | Default: `boogiepop-api-streamlit-svc` |

## Infra previa (Terraform)

En `boogiepop-backend/infra/terraform`:

```hcl
enable_frontend_ecs  = true
enable_streamlit_ecs = true
```

Tras `terraform apply`, outputs útiles: `ecr_streamlit_url`, `ecs_streamlit_service_name`, `streamlit_http_embed_url`.

## Hub (manifest S3)

No hace falta redeploy del host. Publicá el catálogo con la URL de embed:

```powershell
# desde boogiepop-host/
.\scripts\upload-hub-manifest-aws.ps1
```

`iframeUrl` de prod (Modo A HTTP):  
`http://<alb-dns>/streamlit/?embed=true`

## Verificación

1. ECR `boogiepop-streamlit:latest` con fecha reciente.
2. ECS `boogiepop-api-streamlit-svc`: `runningCount == 1`.
3. ALB target group `boogiepop-stlit-tg`: healthy en `/streamlit/_stcore/health`.
4. Hub → login → card Streamlit → `/hub/app/streamlit-dashboard`.
