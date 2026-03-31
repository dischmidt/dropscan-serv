---
description: "Build OpenClaw phase 1 foundation files (context, output, API client)."
name: "OpenClaw Phase 1"
argument-hint: "Create phase-1 files"
agent: "agent"
---
Implement phase 1 for OpenClaw in this workspace.

Goals:
1. Ensure [context.py](../../context.py) defines an AppContext dataclass with client and selected scanbox state.
2. Ensure [output.py](../../output.py) provides a global output handler controlled by FORMATTNG (fallback FORMATTING) supporting: json, rich, txt, markdown.
3. Ensure [client.py](../../client.py) wraps Dropscan API calls with bearer auth using DROPSCAN_API_KEY.

Constraints:
- Python 3 only.
- Use click exceptions for user-facing API errors.
- Keep changes minimal and focused.

References:
- [requirements.txt](../../requirements.txt)
- [.env.example](../../.env.example)
