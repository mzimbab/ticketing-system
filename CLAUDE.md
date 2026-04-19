# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
python travel_todo.py <command> [arguments]
```

Commands: `list`, `add <description>`, `complete <id>`, `delete <id>`, `flight <number>`, `help`

Todo data persists to `todos.json` in the working directory.

## Architecture

Single-file CLI app (`travel_todo.py`). Commands map directly to `cmd_*` functions via the `COMMANDS` dict. `load_todos`/`save_todos` handle all persistence. Flight data is a static in-memory dict (no external API).

## GitHub Actions

Two workflows are configured:

- **`claude.yml`** — Claude PR Assistant: responds when `@claude` is mentioned in issues, PR comments, or reviews. Requires `CLAUDE_CODE_OAUTH_TOKEN` secret.
- **`claude-code-review.yml`** — Automatic code review on every PR open/update using the `code-review` plugin.
