import click

from context import AppContext
from output import output


@click.group("scanbox")
def scanbox_group() -> None:
    """Manage scanboxes."""


@scanbox_group.command("list")
@click.pass_context
def list_scanboxes(ctx: click.Context) -> None:
    app: AppContext = ctx.obj
    scanboxes = app.client.get("/scanboxes")
    rows = []
    for sb in scanboxes:
        rows.append(
            {
                "id": sb.get("id"),
                "number": sb.get("number"),
                "auto_scan": sb.get("auto_scan"),
                "auto_destroy": sb.get("auto_destroy"),
                "recipients": len(sb.get("recipients") or []),
            }
        )
    output.table(rows)


@scanbox_group.command("select")
@click.argument("scanbox_id", type=int)
@click.pass_context
def select_scanbox(ctx: click.Context, scanbox_id: int) -> None:
    app: AppContext = ctx.obj
    scanboxes = app.client.get("/scanboxes")
    if not any(sb.get("id") == scanbox_id for sb in scanboxes):
        raise click.ClickException(f"Scanbox {scanbox_id} is not available for this account.")
    app.scanbox_id = scanbox_id
    output.message(f"Scanbox {scanbox_id} selected.")


@scanbox_group.command("info")
@click.pass_context
def scanbox_info(ctx: click.Context) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    scanboxes = app.client.get("/scanboxes")
    scanbox = next((sb for sb in scanboxes if sb.get("id") == scanbox_id), None)
    if not scanbox:
        raise click.ClickException(f"Selected scanbox {scanbox_id} not found.")

    # For table-based formats, render recipients as a separate table instead of JSON text.
    if output.format == "json":
        output.detail(scanbox)
        return

    details = dict(scanbox)
    recipients = details.pop("recipients", []) or []
    output.detail(details)

    output.message("Recipients:")
    recipient_rows = [
        {
            "id": recipient.get("id"),
            "name": recipient.get("name"),
        }
        for recipient in recipients
    ]
    output.table(recipient_rows)
