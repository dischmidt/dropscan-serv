---
description: "Build OpenClaw phase 2 command modules for scanboxes, mailings, actions, recipients, and forwarding addresses."
name: "OpenClaw Phase 2"
argument-hint: "Create phase-2 command modules"
agent: "agent"
---
Implement phase 2 for OpenClaw command modules in [commands/](../../commands/).

Goals:
1. Implement scanbox commands: list, select, info.
2. Implement mailing commands: list, show, envelope, pdf, plaintext, zip, delete (destroy action request).
3. Implement action commands: scan, forward, destroy, cancel.
4. Implement recipients commands: list, show.
5. Implement addresses commands: register, show.

Constraints:
- Reuse [output.py](../../output.py) for all user-visible output.
- Reuse [client.py](../../client.py) for API calls.
- Commands requiring a scanbox must call context validation.
- Keep endpoint paths aligned with API docs in [API Documentation.md](../../API Documentation.md).
