# Automatizar publicación en Confluence (desde pipeline en `main`)

Estado: **no implementado** en `.gitlab-ci.yml`; esta nota define el camino para cuando el equipo quiera **sincronizar** `docs/confluence/*.md` al espacio Confluence en cada merge a `main` o en tag de release.

## Objetivo

Job de CI que, tras un evento acordado (`main` o `v*`), suba o actualice páginas Confluence vía **REST API** de Atlassian.

## Prerrequisitos

1. Páginas destino creadas una vez en Confluence (padre + hijas) y sus **PAGE_ID** anotados.
2. Token de servicio con permisos de contenido en el espacio (`CONFLUENCE_SPACE_KEY`).
3. Variables en GitLab (masked / protected): `CONFLUENCE_BASE_URL`, credenciales, mapping `archivo_md → page_id` (variables o JSON versionado fuera del repo sensible).

## Enfoques técnicos

| Opción | Notas |
|--------|--------|
| Script `curl` + JSON `storage` (XHTML) | Requiere conversión fiable Markdown→HTML o mantener HTML en pipeline. |
| Cliente Python `requests` + API v2 Cloud | Documentación oficial Atlassian Content API. |
| App marketplace (Markdown sync) | Menos código, coste/licencia terceros. |
| **Servidor MCP (Cursor, Claude Desktop…)** | Asistente puede crear/actualizar páginas *interactivamente*; ver sección siguiente. No reemplaza el job de CI si querés automatizar sólo desde GitLab.

## MCP desde Cursor o cliente compatible (uso interactivo)

**Sí**, podés usar **Model Context Protocol** para que un asistente con herramientas Confluence cargue `docs/confluence/*.md`. Esto suele hacerse **desde tu máquina**, con tus credenciales; **los runners de CI no ejecutan MCP de Cursor** — para `push → main → Confluence sin humano`, seguí el flujo REST del principio del documento.

### Opción recomendada — Atlassian **Rovo** MCP Server (Cloud, oficial)

Guías Atlassian relevantes:

- [Getting started](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)
- [Setting up IDEs (incluye Cursor)](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-ides/)
- [OAuth 2.1](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/)

**Endpoint a usar**: `https://mcp.atlassian.com/v1/mcp/authv2` — Atlassian recomienda dejar atrás rutas SSE antiguas (`/v1/sse` deja de soportarse a partir del **30 de junio de 2026**, según las mismas notas).

**Requisitos en tu equipo**

- Sitio Atlassian Cloud con **Confluence** (y opcionalmente Jira/Compass).
- Para el flujo con proxy local: **Node.js 18+** y `npx` (solo si usás la variante Cursor antigua / `mcp-remote`).
- Para OAuth: cualquier navegador moderno; si querés autenticar con **Brave**, usalo como navegador predeterminado durante el primer login (véase siguiente subsección).
- Opcionalmente: [API token](https://id.atlassian.com/manage-profile/security/api-tokens?autofillToken&expiryDays=max&appId=mcp&selectedScopes=all) si tu **admin organización** [habilitó autenticación por token MCP](https://support.atlassian.com/security-and-access-policies/docs/control-atlassian-rovo-mcp-server-settings/). Si ese modo está **desactivado** en tenant, será obligatorio **OAuth 2.1**.

#### Cursor — configuración (según soporte MCP de tu versión)

**Variante 1 (preferida cuando Cursor permite servidor por URL)**

En Cursor → MCP, añadí una entrada equivalente a (ajustá nombre de servidor si querés otro alias):

```json
"Atlassian-MCP-Server": {
  "url": "https://mcp.atlassian.com/v1/mcp/authv2"
}
```

Lo crítico es la **URL** exacta de arriba.

**Variante 2 (Cursor antiguo o si la URL remota falla)**

Usá el proxy **`mcp-remote`** con Node (`npx`):

```json
"Atlassian-Rovo-MCP": {
  "command": "npx",
  "args": [
    "-y",
    "mcp-remote@latest",
    "https://mcp.atlassian.com/v1/mcp/authv2"
  ]
}
```

Guardá la config, reiniciá la sesión MCP de Cursor si hace falta y probá algo mínimo (por ejemplo preguntas sobre espacios o páginas Confluence donde tengas permiso).

Más información del cliente: [Cursor — MCP](https://docs.cursor.com/en/context/mcp).

#### OAuth con **Brave**

El MCP abre OAuth en el navegador que tu SO elija como predeterminado para enlaces HTTPS:

1. **Windows**: *Configuración → Aplicaciones → Aplicaciones predeterminadas* → establecé **Brave** como navegador predeterminado **antes** de conectar MCP; tras el consentimiento Atlassian podés restaurar otro navegador si querés (el token queda gestionado por Cursor / `mcp-remote`).
2. Si el callback falla (“redirect”, localhost): permití redirects y revisá políticas VPN / [IP allowlist](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/) corporativos.
3. **Brave Shields** suele ser compatible con login Atlassian; si algo se corta silenciosamente, probá Shields más relajados solo para dominios `.atlassian.net` durante el login.

Tu **admin organización** puede exigir [allowlist de dominios para el Rovo MCP Server](https://support.atlassian.com/security-and-access-policies/docs/available-atlassian-rovo-mcp-server-domains/). El primer usuario con permiso adecuado debe completar el consentimiento inicial (instalación JIT de la integración MCP en el tenant).

---

### Opción alternativa — Servidor MCP comunitario (API token por env)

Proyectos comunitarios como [**sooperset/mcp-atlassian**](https://github.com/sooperset/mcp-atlassian) exponen herramientas como `confluence_create_page` / `confluence_update_page`, Confluence Cloud o Data Center ([PyPI](https://pypi.org/project/mcp-atlassian/)).

Ejemplo de idea de configuración (no pegues tokens en el repo; usá Variables de usuario o entrada segura del cliente MCP):

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "CONFLUENCE_URL": "https://tu-empresa.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "usuario@tu-empresa.com",
        "CONFLUENCE_API_TOKEN": "(token de cuenta Atlassian)"
      }
    }
  }
}
```

Requisitos: **Python/`uv`/uvx** instalados donde corre el proceso MCP, cuenta con permiso de escritura en el espacio donde van las páginas, y formato de cuerpo que acepte el servidor (muchas páginas se suben mejor **con Markdown convirtiendo a storage/HTML** según soporte del tool). Algunas versiones piden también variables **Jira** aunque solo uses Confluence — revisá el README del servidor.

### Cómo encaja con esta carpeta del seed

Tras tener el MCP operativo en Cursor Settings → MCP, podés pedir al agente subir/sync **archivos concretos** de `docs/confluence/` contra **page IDs** o padre de espacio que definas por proyecto. Mantener el mismo **mapa** que en [`README.md`](README.md) ayuda.

## Disparadores sugeridos

- Pipeline en **tag** `v*.*.*` tras acuerdo de release (evita ruido en cada commit a `main`).
- O job manual `publish-docs` con `workflow_dispatch` / botón en GitLab.

## Seguridad

No commitear tokens. Rotar PAT periódicamente. Limitar job a ref protegida y rol mínimo en Confluence.

## Referencia API

- [Confluence Cloud REST: update content](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-content/#api-wiki-rest-api-content-id-put)
