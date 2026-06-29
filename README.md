# Dropscan CLI

Python 3 CLI for Dropscan API v1.

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
- `DROPSCAN_SCANBOX` (optional): default scanbox ID used by scanbox-dependent commands
- `FORMATTNG` (optional): `json`, `rich`, `txt`, `markdown` (case-insensitive)
- `FORMATTING` (optional fallback): same values, used only if `FORMATTNG` is unset

Scanbox selection precedence for scanbox-dependent commands:
- `--scanbox <id>` (highest)
- selected scanbox in current session (`scanbox select <id>`) or `DROPSCAN_SCANBOX`

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
./dropscan-serv
```

Prompt:
```text
dropscan>
```

## Basic Workflow
```text
scanbox list
scanbox select 12345
mailings list --scanbox 12345
mailings show <uuid|last|last-N> --scanbox 12345
mailings pdf <uuid|last|last-N> --scanbox 12345 -o file.pdf
mailings plaintext <uuid|last|last-N> --scanbox 12345
action scan <uuid> --scanbox 12345
action forward <uuid> --scanbox 12345 --address-id <address_id> --date 2026-04-01
```

## Commands

### Scanboxes
- `scanbox list`
- `scanbox select <scanbox_id>`
- `scanbox info [--scanbox <scanbox_id>]`

`scanbox info` behavior:
- In `txt`, `rich`, and `markdown` formats, recipients are rendered as a dedicated recipients table.
- In `json` format, the full scanbox object is printed as JSON.

### Mailings
- `mailings list [--scanbox <scanbox_id>] [--status <status>] [--older-than <uuid>]`
- `mailings show <uuid|last|last-N> [--scanbox <scanbox_id>]`
- `mailings envelope <uuid|last|last-N> [--scanbox <scanbox_id>] [-o <path>]`
- `mailings pdf <uuid|last|last-N> [--scanbox <scanbox_id>] [-o <path>] [--uuid]`
- `mailings plaintext <uuid|last|last-N> [--scanbox <scanbox_id>] [-o <path>] [--uuid]`
- `mailings zip <uuid|last|last-N> [--scanbox <scanbox_id>] [-o <path>] [--uuid]`
- `mailings delete <uuid|last|last-N> [--scanbox <scanbox_id>] [--yes]`

`last` and `last-N` resolve against `mailings list` order (`last` = top/youngest mailing, `last-1` = second row, etc.).

Export naming (`pdf`, `plaintext`, `zip`):
- default filename uses mailing `name` as shown by `mailings show` (extension adjusted by command)
- pass `--uuid` to use the previous UUID-based filename behavior
- pass `-o/--output` to fully control target path/filename

Status values:
- `received`
- `scan_requested`
- `scanned`
- `destroy_requested`
- `destroyed`
- `forward_requested`
- `forwarded`

### Actions
- `action scan <uuid> [--scanbox <scanbox_id>]`
- `action forward <uuid> [--scanbox <scanbox_id>] --address-id <id> --date <YYYY-MM-DD>`
- `action destroy <uuid> [--scanbox <scanbox_id>] [--yes]`
- `action cancel <mailing_uuid> <action_id> [--scanbox <scanbox_id>]`

### Recipients
- `recipients list [--scanbox <scanbox_id>]`
- `recipients show <recipient_id> [--scanbox <scanbox_id>]`

### Forwarding Addresses
- `addresses register [options]`
- `addresses show <address_id>`

Note: the public API does not provide an endpoint to list all registered forwarding addresses.

## Notes
- Email forwarding is not exposed as a dedicated endpoint in public Dropscan API v1.
- Physical forwarding is supported through `action forward` with forwarding address + date.
- Destroying mail is irreversible. Use confirmation or `--yes` intentionally.
