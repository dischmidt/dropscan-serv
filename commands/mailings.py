import click
import os
import re

from context import AppContext
from output import output


_MAILING_STATUSES = [
    "received",
    "scan_requested",
    "scanned",
    "destroy_requested",
    "destroyed",
    "forward_requested",
    "forwarded",
]


_LAST_MAILING_PATTERN = re.compile(r"^last(?:-(\d+))?$")


def _sanitize_filename(value: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip().rstrip(".")
    return sanitized or "mailing"


def _mailing_default_filename(mailing: dict, uuid: str, extension: str, use_uuid: bool) -> str:
    if use_uuid:
        base_name = uuid
    else:
        show_name = str(mailing.get("pdf_name") or "").strip()
        if not show_name:
            show_name = str(mailing.get("name") or "").strip()
        if show_name:
            sanitized = _sanitize_filename(show_name)
            root, ext = os.path.splitext(sanitized)
            if root and ext.lower() in {".pdf", ".txt", ".zip"}:
                base_name = root
            else:
                base_name = sanitized
        else:
            base_name = uuid
    return f"{base_name}{extension}"


def _resolve_mailing_uuid(app: AppContext, uuid_or_alias: str, scanbox_id: int | None = None) -> str:
    match = _LAST_MAILING_PATTERN.match(uuid_or_alias)
    if not match:
        return uuid_or_alias

    index = int(match.group(1) or "0")
    if index < 0:
        raise click.ClickException("Mailing alias index cannot be negative.")

    resolved_scanbox_id = app.resolve_scanbox(scanbox_id)
    mailings = app.client.get(f"/scanboxes/{resolved_scanbox_id}/mailings")

    if index >= len(mailings):
        raise click.ClickException(
            f"Mailing alias '{uuid_or_alias}' is out of range. "
            f"Only {len(mailings)} mailing(s) available."
        )

    resolved_uuid = mailings[index].get("uuid")
    if not resolved_uuid:
        raise click.ClickException(
            f"Mailing alias '{uuid_or_alias}' could not be resolved because the mailing has no UUID."
        )

    return resolved_uuid


@click.group("mailings")
def mailings_group() -> None:
    """Inspect and operate on mailings."""


@mailings_group.command("list")
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.option("--status", "status", type=click.Choice(_MAILING_STATUSES, case_sensitive=False))
@click.option("--older-than", type=str)
@click.pass_context
def list_mailings(
    ctx: click.Context,
    scanbox_id: int | None,
    status: str | None,
    older_than: str | None,
) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    params = {
        "current_status": status,
        "older_than": older_than,
    }
    data = app.client.get(f"/scanboxes/{scanbox_id}/mailings", params=params)
    rows = []
    for item in data:
        rows.append(
            {
                "uuid": item.get("uuid"),
                "status": item.get("status"),
                "recipient_id": item.get("recipient_id"),
                "received_at": item.get("received_at"),
                "scan_requested_at": item.get("scan_requested_at"),
                "scanned_at": item.get("scanned_at"),
                "forward_requested_for": item.get("forward_requested_for"),
            }
        )
    output.table(rows)


@mailings_group.command("show")
@click.argument("uuid", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.pass_context
def show_mailing(ctx: click.Context, uuid: str, scanbox_id: int | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    uuid = _resolve_mailing_uuid(app, uuid, scanbox_id=scanbox_id)
    data = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}")
    output.detail(data)


@mailings_group.command("envelope")
@click.argument("uuid", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.option("-o", "--output", "output_path", type=str)
@click.pass_context
def envelope(
    ctx: click.Context,
    uuid: str,
    scanbox_id: int | None,
    output_path: str | None,
) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    uuid = _resolve_mailing_uuid(app, uuid, scanbox_id=scanbox_id)
    data = app.client.get_binary(f"/scanboxes/{scanbox_id}/mailings/{uuid}/envelope")
    output.save_binary(data, output_path, f"{uuid}_envelope.jpg")


@mailings_group.command("pdf")
@click.argument("uuid", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.option("-o", "--output", "output_path", type=str)
@click.option("--uuid", "use_uuid", is_flag=True, help="Use UUID as output filename.")
@click.pass_context
def pdf(
    ctx: click.Context,
    uuid: str,
    scanbox_id: int | None,
    output_path: str | None,
    use_uuid: bool,
) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    uuid = _resolve_mailing_uuid(app, uuid, scanbox_id=scanbox_id)
    default_name = f"{uuid}.pdf"
    if not use_uuid and not output_path:
        mailing = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}")
        default_name = _mailing_default_filename(mailing, uuid, ".pdf", use_uuid)
    data = app.client.get_binary(f"/scanboxes/{scanbox_id}/mailings/{uuid}/pdf")
    output.save_binary(data, output_path, default_name)


@mailings_group.command("plaintext")
@click.argument("uuid", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.option("-o", "--output", "output_path", type=str)
@click.option("--uuid", "use_uuid", is_flag=True, help="Use UUID as output filename.")
@click.pass_context
def plaintext(
    ctx: click.Context,
    uuid: str,
    scanbox_id: int | None,
    output_path: str | None,
    use_uuid: bool,
) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    uuid = _resolve_mailing_uuid(app, uuid, scanbox_id=scanbox_id)
    default_name = f"{uuid}.txt"
    if not use_uuid and not output_path:
        mailing = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}")
        default_name = _mailing_default_filename(mailing, uuid, ".txt", use_uuid)
    text = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}/plaintext", expect_json=False)
    output.save_text(text, output_path, default_name)


@mailings_group.command("zip")
@click.argument("uuid", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.option("-o", "--output", "output_path", type=str)
@click.option("--uuid", "use_uuid", is_flag=True, help="Use UUID as output filename.")
@click.pass_context
def zip_files(
    ctx: click.Context,
    uuid: str,
    scanbox_id: int | None,
    output_path: str | None,
    use_uuid: bool,
) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    uuid = _resolve_mailing_uuid(app, uuid, scanbox_id=scanbox_id)
    default_name = f"{uuid}.zip"
    if not use_uuid and not output_path:
        mailing = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}")
        default_name = _mailing_default_filename(mailing, uuid, ".zip", use_uuid)
    data = app.client.get_binary(f"/scanboxes/{scanbox_id}/mailings/{uuid}/zip")
    output.save_binary(data, output_path, default_name)


@mailings_group.command("delete")
@click.argument("uuid", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt.")
@click.pass_context
def delete_mailing(ctx: click.Context, uuid: str, scanbox_id: int | None, yes: bool) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    uuid = _resolve_mailing_uuid(app, uuid, scanbox_id=scanbox_id)
    if not yes:
        click.confirm("Permanently destroy this mailing? This cannot be undone.", abort=True)
    result = app.client.post(
        f"/scanboxes/{scanbox_id}/mailings/{uuid}/action_requests",
        payload={"action_type": "destroy"},
    )
    output.detail(result)
