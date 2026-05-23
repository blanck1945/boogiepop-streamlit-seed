# Manifest de infra protegida

[`seed-protected-paths.txt`](seed-protected-paths.txt) es la lista compartida que usan:

- el job **`protect_seed_manifest`** definido en [`.gitlab-ci.yml`](../.gitlab-ci.yml) (MR y ramas mergeables), y  
- opcionalmente el hook local `pre-commit` ([`.pre-commit-config.yaml`](../.pre-commit-config.yaml)).

Las rutas están pensadas sólo como **infra de plataforma** (build, entrada Streamlit garantizada por `configure_page`, control de dependencias pinned, CI/GitLab y los propios chequeos para evitar desactivarlos inadvertidamente). El contenido de producto día a día vive típicamente en `app/Home.py`, `app/pages/**` y la documentación de usuario.

Los mantenedores del seed deben alinear estos patrones cuando:

1. muevan rutas públicas esperadas (`Home.py`, Dockerfile, etc.);
2. añadan archivos infra nuevos obligatorios;
3. necesiten crear excepciones documentadas sólo mediante los mecanismos descritos en [README § Protección de infra](../README.md).
