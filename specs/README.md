# Specs opcionales (features documentadas)

Esta carpeta es **opcional**. Sirve para ordenar trabajo tipo “spec-kit lite” antes de cambiar código: una subcarpeta por feature enumerada (`nnn`-prefijo estable) contiene SPEC/PLAN/TASKS en Markdown **sin ejecutar tooling extra**.

Convención sugerida:

```text
specs/
├── README.md                         # Este archivo
└── <nnn>-<slug-corto>/
    ├── SPEC.md                       # Qué queremos lograr (desde plantilla)
    ├── PLAN.md                       # Cómo lo implementamos
    └── TASKS.md                      # Lista verificable
```

Ejemplo de nombre válido para la próxima feature libre cuando existan pocas especificaciones: `001-maqueta-reportes/` (adaptá `001` incrementalmente cuando agregues carpetas nuevas si querés orden lexicográfico simple).

Las plantillas y el flujo detallado se describen en:

- Índice: [spec-kit/README.md](../spec-kit/README.md)
- Plantilla copiable: [spec-kit/templates/feature-spec.template.md](../spec-kit/templates/feature-spec.template.md)
- Workflow: [spec-kit/workflows/spec-driven-lite.md](../spec-kit/workflows/spec-driven-lite.md)

Reglas siempre aplicables siguen siendo las de **[AGENTS.md](../AGENTS.md)**.
