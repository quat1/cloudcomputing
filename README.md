# cloudcomputing — хаб агентов для моих проектов

Репозиторий-пульт: в `.claude/agents/` лежат субагенты Claude Code, по одному
на проект. Открываю `claude` здесь, пишу задачу — нужный агент идёт в
репозиторий проекта и делает её.

## Быстрый старт

```bash
git clone https://github.com/quat1/cloudcomputing
cd cloudcomputing
scripts/clone.sh              # склонировать все проекты в workspace/
claude                        # /agents покажет 7 агентов
```

Проекты уже лежат отдельно (например, в `~/projects/`)? Тогда вместо клона:

```bash
claude --add-dir ~/projects/zerdeli-website --add-dir ~/projects/aqbota_repo
```

Чтобы агенты работали из любой папки, а не только из хаба:

```bash
scripts/install-agents.sh     # копирует в ~/.claude/agents и ~/.claude/skills
```

Примеры задач:

```
/task zerdeli добавь на страницу контактов карту 2GIS
/task aqbota в tempo исправь падение при пустом дневнике
@torge-dev опиши экраны онбординга продавца как спецификацию
проверь последний коммит в zerdeli      ← запустит project-reviewer
```

## Что внутри

| Путь | Назначение |
| --- | --- |
| `CLAUDE.md` | правила маршрутизации задач по агентам |
| `.claude/agents/*.md` | агенты: `zerdeli-dev`, `aqbota-dev`, `torge-dev`, `keysora-dev`, `qep-dev`, `web-dev`, `project-reviewer` |
| `.claude/skills/task/` | команда `/task <проект> <задача>` |
| `projects/registry.json` | реестр проектов: репозиторий, папка, стек, агент |
| `scripts/clone.sh` | клонирует проекты из реестра в `workspace/` |
| `scripts/install-agents.sh` | копирует агентов в `~/.claude/agents`, чтобы они работали из любой папки |
| `workspace/` | локальные клоны проектов (в git не попадают) |
| `.claude/agent-memory/` | память агентов между сессиями (создаётся сама) |

## Добавить новый проект

1. Добавить запись в `projects/registry.json`.
2. Скопировать ближайший по стеку агент из `.claude/agents/` под новым именем
   и описать проект: стек, структура, команды проверки, правила.
3. Добавить строку в таблицу проектов в `CLAUDE.md`.
