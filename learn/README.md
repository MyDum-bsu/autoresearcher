# `learn/` — Мост «Авторесерчер v2 ↔ LearnHarness v0.7.0»

> **Контракт R5 (`#1162`):** ноль правок ядра LearnHarness и ноль прямой записи в `nodes.jsonl` / `chains.jsonl`. Запись идёт строго через HTTP API LearnHarness (`POST /api/graph/import`, `POST /api/chats`), чтение — через `GET /api/graph` и официальный read-only скрипт `skills/learnharness/scripts/graph.py`.

## Модули

- [`build_pack.py`](build_pack.py) — сборка и валидация 4-файлового экспортного пакета из `research/guides/<topic>/` с иерархией относительных путей `ARO/<track>/<topic>/<file>.md`, проверкой `validNotesPath` и опциональным гейтом G5 (`--validate-gate`).
- [`push_to_lh.py`](push_to_lh.py) — отправка пакета через `POST /api/graph/import` (multipart `files` + `paths`, по умолчанию идемпотентно: неизменённые файлы пропускаются как `skipped_unchanged`, принудительный переимпорт — `--force`) и команда `aro study <topic> --mode teach|practice`, создающая сессию через `POST /api/chats` (для `practice` — с `kind: "practice"` и предзаполненным `graphContext` из пропозиций топика).
- [`pull_lh_context.py`](pull_lh_context.py) — read-only адаптер поверх штатного `skills/learnharness/scripts/graph.py --data-dir ... --format json` для чтения уже усвоенных узлов и цепочек по `ARO/` без изменения данных.

## Основные команды

```bash
# 1. Проверить и собрать пакет (dry-run манифест)
python3 -B -m learn.build_pack 01-bridge-packet-01 --validate-gate --json

# 2. Импортировать пакет в локальный LearnHarness v0.7.0 (или --dry-run)
python3 -B -m learn.push_to_lh push 01-bridge-packet-01 --url http://127.0.0.1:3000

# 3. Запустить Teach или Practice сессию (также доступно как `aro study ...`)
python3 -B -m learn.push_to_lh study 01-bridge-packet-01 --mode practice --url http://127.0.0.1:3000

# 4. Прочитать контекст ARO из графа LearnHarness (строго read-only)
python3 -B -m learn.pull_lh_context --data-dir ~/.config/LearnHarness/data --topic 01-bridge-packet-01 --format markdown

# 5. Полный прогон unit + изолированного E2E теста против реального LearnHarness v0.7.0
make verify-learn
```

> Все автотесты запускаются строго на временном изолированном `LH_DATA_DIR` и проверяют неизменность живого профиля `~/.config/LearnHarness/data`.
