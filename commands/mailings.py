import click

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


@click.group("mailings")
def mailings_group() -> None:
    """Inspect and operate on mailings."""


@mailings_group.command("list")
@click.option("--status", "status", type=click.Choice(_MAILING_STATUSES, case_sensitive=False))
@click.option("--older-than", type=str)
@click.pass_context
def list_mailings(ctx: click.Context, status: str | None, older_than: str | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
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
@click.pass_context
def show_mailing(ctx: click.Context, uuid: str) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    data = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}")
    output.detail(data)


@mailings_group.command("envelope")
@click.argument("uuid", type=str)
@click.option("-o", "--output", "output_path", type=str)
@click.pass_context
def envelope(ctx: click.Context, uuid: str, output_path: str | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    data = app.client.get_binary(f"/scanboxes/{scanbox_id}/mailings/{uuid}/envelope")
    output.save_binary(data, output_path, f"{uuid}_envelope.jpg")


@mailings_group.command("pdf")
@click.argument("uuid", type=str)
@click.option("-o", "--output", "output_path", type=str)
@click.pass_context
def pdf(ctx: click.Context, uuid: str, output_path: str | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    data = app.client.get_binary(f"/scanboxes/{scanbox_id}/mailings/{uuid}/pdf")
    output.save_binary(data, output_path, f"{uuid}.pdf")


@mailings_group.command("plaintext")
@click.argument("uuid", type=str)
@click.pass_context
def plaintext(ctx: click.Context, uuid: str) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    text = app.client.get(f"/scanboxes/{scanbox_id}/mailings/{uuid}/plaintext", expect_json=False)
    output.message(text)


@mailings_group.command("zip")
@click.argument("uuid", type=str)
@click.option("-o", "--output", "output_path", type=str)
@click.pass_context
def zip_files(ctx: click.Context, uuid: str, output_path: str | None) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    data = app.client.get_binary(f"/scanboxes/{scanbox_id}/mailings/{uuid}/zip")
    output.save_binary(data, output_path, f"{uuid}.zip")


@mailings_group.command("delete")
@click.argument("uuid", type=str)
@click.option("--yes", is_flag=True, help="Skip confirmation prompt.")
@click.pass_context
def delete_mailing(ctx: click.Context, uuid: str, yes: bool) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    if not yes:
        click.confirm("Permanently destroy this mailing? This cannot be undone.", abort=True)
    result = app.client.post(
        f"/scanboxes/{scanbox_id}/mailings/{uuid}/action_requests",
        payload={"action_type": "destroy"},
    )
    output.detail(result)
