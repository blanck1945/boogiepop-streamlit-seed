#!/usr/bin/env sh
# Valida pares fuente/target de MR según política ramas vivas develop / staging / main.
#
# Variables esperadas en pipeline de merge request GitLab:
#   CI_MERGE_REQUEST_SOURCE_BRANCH_NAME
#   CI_MERGE_REQUEST_TARGET_BRANCH_NAME
#   CI_MERGE_REQUEST_LABELS (opcional, para bypass)
#
# Bypass emergencia sólo equipo plataforma:
#   CI/CD masked: BRANCH_FLOW_BYPASS=1
# Etiquetas MR opcionales: branch-flow-bypass

set -eu

if [ "${BRANCH_FLOW_BYPASS:-}" = "1" ]; then
	echo "branch-flow: bypass activado (documentar motivo)." >&2
	exit 0
fi

labels="${CI_MERGE_REQUEST_LABELS:-}"
case "$labels" in
*"branch-flow-bypass"* | *"branch_flow_bypass"*)
	echo "branch-flow: bypass etiqueta MR aplicado." >&2
	exit 0
	;;
esac

SOURCE="${CI_MERGE_REQUEST_SOURCE_BRANCH_NAME:-}"
TARGET="${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-}"

if [ -z "$SOURCE" ] || [ -z "$TARGET" ]; then
	echo "branch-flow: falta SOURCE/TARGET de MR GitLab para validación." >&2
	exit 1
fi

case "$TARGET" in
develop)
	case "$SOURCE" in
	feature/*|feat/*|fix/*|docs/*|chore/*|hotfix/*|renovate/*|dependabot*)
		exit 0
		;;
	*)
		echo "branch-flow: a **develop** sólo merges desde ramas trabajo (feature/*, feat/*, fix/*, docs/*, chore/*, hotfix/*, renovate/*, dependabot*). Actual: '$SOURCE'." >&2
		exit 1
		;;
	esac
	;;
staging)
	if [ "$SOURCE" = "develop" ]; then
		exit 0
	fi
	echo "branch-flow: a **staging** sólo merges desde **develop**. Actual desde '$SOURCE'." >&2
	exit 1
	;;
main)
	echo "branch-flow: no se permite MR hacia **main**. Promové con tag desde línea **staging** (docs/gitlab-branching.md)." >&2
	exit 1
	;;
*)
	echo "branch-flow: target MR no gestionado ('$TARGET')." >&2
	exit 1
	;;
esac
