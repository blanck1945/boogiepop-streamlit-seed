---
confluence_hint: página "GitLab CI and branch policy"
---

# GitLab, ramas y seguridad infra (resumen)

La referencia técnica detallada está en el repo en **`docs/gitlab-branching.md`**. Esta página sirve como resumen ejecutivo para Confluence.

## Ramas modelo

| Rama | Rol breve |
|------|-----------|
| `develop` | Integración diaria desde ramas de trabajo (`feature/*`, etc., según validación MR). |
| `staging` | Pre-producción; MR permitido sólo desde `develop`. |
| `main` | Producción; en la plantilla actual los **MR hacia `main` fallan en CI**; la promoción se documenta como vía **tag / job de release** (definir con plataforma). |

## Jobs de pipeline relevantes

- **`protect_seed_manifest`**: compara el diff con `maintainers/seed-protected-paths.txt`.
- **`merge_request_branch_flow`**: valida pares fuente/target de MR según política anterior.

Bypasses de emergencia: ver `README.md` y `AGENTS.md` del repositorio (etiquetas y variables CI).

## Qué debe configurarse en GitLab (UI)

Ramas protegidas, merges sólo con pipeline verde, `CODEOWNERS` activo cuando el equipo descomente owners reales, y **Merge request pipelines** habilitados.
