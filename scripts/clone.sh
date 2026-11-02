#!/usr/bin/env bash
# Клонирует проекты из projects/registry.json в workspace/<name>.
#
#   scripts/clone.sh            # все проекты
#   scripts/clone.sh zerdeli    # один проект (по name из registry.json)
#
# Нужен git и jq (brew install jq / apt install jq).

set -euo pipefail

HUB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="$HUB_DIR/projects/registry.json"
WORKSPACE="${PROJECTS_DIR:-$HUB_DIR/workspace}"

command -v jq >/dev/null || { echo "Нужен jq: brew install jq (macOS) или apt install jq (Linux)" >&2; exit 1; }

mkdir -p "$WORKSPACE"

filter="${1:-}"

jq -r '.projects[] | select(.repo != null) | "\(.name)\t\(.repo)\t\(.dir)"' "$REGISTRY" |
while IFS=$'\t' read -r name repo dir; do
  if [[ -n "$filter" && "$filter" != "$name" && "$filter" != "$dir" ]]; then
    continue
  fi
  target="$WORKSPACE/$dir"
  if [[ -d "$target/.git" ]]; then
    echo "✓ $name — уже есть: $target"
    continue
  fi
  echo "→ $name — клонирую $repo в $target"
  git clone "$repo" "$target"
done

echo
echo "Готово. Проекты лежат в: $WORKSPACE"
