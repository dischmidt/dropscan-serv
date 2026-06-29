import click

from context import AppContext
from output import output


@click.group("recipients")
def recipients_group() -> None:
    """Manage scanbox recipients."""


@recipients_group.command("list")
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.pass_context
def list_recipients(ctx: click.Context, scanbox_id: int | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    recipients = app.client.get(f"/scanboxes/{scanbox_id}/recipients")
    rows = []
    for recipient in recipients:
        rows.append(
            {
                "id": recipient.get("id"),
                "type": recipient.get("type"),
                "name": recipient.get("name"),
                "firstname": recipient.get("firstname"),
                "lastname": recipient.get("lastname"),
                "created_at": recipient.get("created_at"),
            }
        )
    output.table(rows)


@recipients_group.command("show")
@click.argument("recipient_id", type=str)
@click.option("--scanbox", "scanbox_id", type=int, help="Override scanbox ID for this command.")
@click.pass_context
def show_recipient(ctx: click.Context, recipient_id: str, scanbox_id: int | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.resolve_scanbox(scanbox_id)
    recipient = app.client.get(f"/scanboxes/{scanbox_id}/recipients/{recipient_id}")
    output.detail(recipient)
