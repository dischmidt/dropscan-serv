---
name: dropscan-serv
description: "Build and maintain the OpenClaw Dropscan CLI. Use when working with scanboxes, mailings, recipients, forwarding addresses, API actions, and output formatting in this repository."
argument-hint: "Implement or update Dropscan CLI features"
---

# Dropscan CLI Skill

## Purpose
This skill implements and maintains a Python 3 CLI tool for Dropscan API v1.

## Use When
- You need to add or change scanbox commands.
- You need to list, inspect, download, or destroy mailings.
- You need to register or inspect forwarding addresses.
- You need to add recipient queries.
- You need to adjust output formatting behavior.

## Architecture
- Entry point: [dropscan.py](./dropscan.py)
- API client: [client.py](./client.py)
- Runtime context: [context.py](./context.py)
- Global output handler: [output.py](./output.py)
- Commands package: [commands](./commands)

## Environment Variables
- `DROPSCAN_API_KEY`: Bearer token used for API authentication.
- `DROPSCAN_API_BASE_URL`: Optional API URL override.
- `FORMATTNG`: Output style selector (`json`, `rich`, `txt`, `markdown`) case-insensitive.
- `FORMATTING`: Fallback alias for output style if `FORMATTNG` is unset.

## Output Rules
Always route user-visible output through the global handler in [output.py](./output.py).

## Command Scope
- `scanbox`: list, select, info
- `mailings`: list, show, envelope, pdf, plaintext, zip, delete
- `action`: scan, forward, destroy, cancel
- `recipients`: list, show
- `addresses`: register, show

## Behavioral Notes
- Wrapper script is `./dropscan-serv` and runs the CLI in the local virtual environment.
- `scanbox info` prints recipients as a dedicated nested table for `txt`, `rich`, and `markdown` output formats.
- API supports forwarding address registration and retrieval by ID; there is no endpoint to list all forwarding addresses.

## Implementation Checklist
1. Confirm required endpoint exists in Dropscan API docs.
2. Add command in the appropriate module in [commands](./commands).
3. Use [client.py](./client.py) for API access.
4. Enforce selected scanbox where required.
5. Use [output.py](./output.py) for all output.
6. Keep errors user-friendly via click exceptions.
