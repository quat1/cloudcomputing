#!/usr/bin/env bash
# Делает агентов и команды из этого репозитория доступными во ВСЕХ проектах
# на этой машине: копирует их в ~/.claude/agents и ~/.claude/skills.
#
#   scripts/install-agents.sh          # скопировать
#   scripts/install-agents.sh --link   # симлинки (изменения в репо подхватываются сразу)
#
# После установки агенты работают, даже если открыть claude прямо в папке проекта
# (например, в zerdeli-website), а не в этом репозитории.

set -euo pipefail

HUB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
USER_CLAUDE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
MODE="${1:-copy}"

mkdir -p "$USER_CLAUDE/agents" "$USER_CLAUDE/skills"

install_one() {
  local src="$1" dst="$2"
  if [[ "$MODE" == "--link" ]]; then
    rm -rf "$dst"
    ln -s "$src" "$dst"
    echo "  link  $dst -> $src"
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "  copy  $dst"
  fi
}

echo "Агенты:"
for f in "$HUB_DIR"/.claude/agents/*.md; do
  install_one "$f" "$USER_CLAUDE/agents/$(basename "$f")"
done

echo "Команды (skills):"
for d in "$HUB_DIR"/.claude/skills/*/; do
  d="${d%/}"
  install_one "$d" "$USER_CLAUDE/skills/$(basename "$d")"
done

echo
echo "Готово. Проверить: запустите claude и наберите /agents"
