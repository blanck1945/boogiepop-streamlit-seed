# Documentación tipo Confluence (Boogiepop Streamlit Seed)

Contenido en **Markdown** pensado para **publicar manualmente en Confluence** (pegar página a página o importación Markdown según vuestra Cloud/Data Center edition) y, más adelante, para **automación** desde pipeline.

## Mapa sugerido de página padre ↔ archivos en este repo

| Página recomendada en Confluence | Archivo fuente aquí |
|-----------------------------------|---------------------|
| Resumen del producto / alcance seed | Este `README.md` + [01-overview.md](01-overview.md) |
| Guía de usuario (desarrollador que adopte el seed) | [02-user-guide.md](02-user-guide.md) |
| Arquitectura técnica | [03-architecture.md](03-architecture.md) |
| Funciones y características del seed | [04-features.md](04-features.md) |
| Pipeline, ramas GitLab y seguridad infra | [05-gitlab-and-ci-security.md](05-gitlab-and-ci-security.md) |
| Referencia operativa (deployment) | [06-deployment-runbook.md](06-deployment-runbook.md) |
| Historial versiones | [CHANGELOG.md](CHANGELOG.md) |

## Consejos rápidos al pegar en Confluence

- **Tablas Markdown** suelen funcionar directo pegando desde editor Markdown de Confluence o vía [**Markdown macro**](https://confluence.atlassian.com/doc/using-markdown-syntax-in-editor-1309688104.html).
- Diagramas **`mermaid`**: usar macro *Mermaid* / *PlantUML* o captura si no hay soporte Cloud.
- **Macros internas**: reemplazar `YOUR_CONFLUENCE_BASE` en enlaces externos al repo/GitLab antes de automatizar.

## Automatización (objetivo: push → `main` → páginas Confluence)

No está cableado en `.gitlab-ci.yml` todavía. La estrategia y variables necesarias están en **[AUTOMATION.md](AUTOMATION.md)** (REST API desde CI más **servidor MCP oficial Atlassian Rovo**, Cursor + OAuth OAuth y opción Brave).

## MCP Atlassian Rovo + Cursor + Brave (rápido)

1. Brave como navegador predeterminado (Windows → Aplicaciones predeterminadas) solo para el primer login.
2. En Cursor, MCP según **[AUTOMATION.md — Rovo](AUTOMATION.md)**: endpoint `https://mcp.atlassian.com/v1/mcp/authv2` o fallback `npx mcp-remote@latest …`.
3. Reiniciá herramientas MCP y concedé permisos en la ventana Brave de Atlassian.
