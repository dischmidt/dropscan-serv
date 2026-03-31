# OpenClaw Dropscan CLI

OpenClaw is a Python 3 CLI for Dropscan API v1.

## Features
- Select a scanbox and list mailings
- Filter mailings by status and pagination marker
- Get mailing details
- Download envelope image, combined PDF, and ZIP of scanned PDFs
- Get plaintext/OCR content of a mailing
- Request actions: scan, forward, destroy
- Cancel requested actions
- Register and retrieve forwarding addresses
- List recipients in a scanbox and retrieve recipient details

## Requirements
- Python 3.10+
- A Dropscan API key with API access enabled

## Setup
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Configure environment:
   - Copy `.env.example` to `.env`
   - Set `DROPSCAN_API_KEY`

## Environment Variables
- `DROPSCAN_API_KEY` (required): Dropscan Bearer API token
- `DROPSCAN_API_BASE_URL` (optional): defaults to `https://api.dropscan.de/v1`
- `FORMATTNG` (optional): `json`, `rich`, `txt`, `markdown` (case-insensitive)
- `FORMATTING` (optional fallback): same values, used only if `FORMATTNG` is unset

## Output Formatting
Global formatting is handled by a single output handler.

- `FORMATTNG=json`: raw JSON
- `FORMATTNG=rich`: rich tables (default)
- `FORMATTNG=txt`: plain text tables
- `FORMATTNG=markdown`: GitHub markdown tables

## Run
```bash
python dropscan.py
```

Recommended (uses the project virtual environment automatically):
```bash
./openclaw
```

Prompt:
```text
dropscan>
```

## Basic Workflow
```text
scanbox list
scanbox select 12345
mailings list
mailings show <uuid>
mailings pdf <uuid> -o file.pdf
action scan <uuid>
action forward <uuid> --address-id <address_id> --date 2026-04-01
```

## Commands

### Scanboxes
- `scanbox list`
- `scanbox select <scanbox_id>`
- `scanbox info`

### Mailings
- `mailings list [--status <status>] [--older-than <uuid>]`
- `mailings show <uuid>`
- `mailings envelope <uuid> [-o <path>]`
- `mailings pdf <uuid> [-o <path>]`
- `mailings plaintext <uuid>`
- `mailings zip <uuid> [-o <path>]`
- `mailings delete <uuid> [--yes]`

Status values:
- `received`
- `scan_requested`
- `scanned`
- `destroy_requested`
- `destroyed`
- `forward_requested`
- `forwarded`

### Actions
- `action scan <uuid>`
- `action forward <uuid> --address-id <id> --date <YYYY-MM-DD>`
- `action destroy <uuid> [--yes]`
- `action cancel <mailing_uuid> <action_id>`

### Recipients
- `recipients list`
- `recipients show <recipient_id>`

### Forwarding Addresses
- `addresses register [options]`
- `addresses show <address_id>`

## Notes
- Email forwarding is not exposed as a dedicated endpoint in public Dropscan API v1.
- Physical forwarding is supported through `action forward` with forwarding address + date.
- Destroying mail is irreversible. Use confirmation or `--yes` intentionally.
