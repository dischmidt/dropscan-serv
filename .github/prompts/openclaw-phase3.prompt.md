---
description: "Build OpenClaw phase 3 entrypoint and documentation."
name: "OpenClaw Phase 3"
argument-hint: "Create phase-3 entrypoint and README"
agent: "agent"
---
Implement phase 3 for OpenClaw.

Goals:
1. Create/verify [dropscan.py](../../dropscan.py) as click_shell entrypoint that loads env, validates DROPSCAN_API_KEY, and registers command groups.
2. Create/verify [README.md](../../README.md) with setup, environment variables, format behavior, and command examples.

Constraints:
- Mention FORMATTNG values: json, rich, txt, markdown.
- Mention fallback support for FORMATTING.
- Keep docs practical and concise.
