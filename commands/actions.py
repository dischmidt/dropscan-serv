import click

from context import AppContext
from output import output


@click.group("action")
def action_group() -> None:
    """Request and manage mailing actions."""


@action_group.command("scan", help="Request opening and scanning of a received mailing.")
@click.argument("uuid", type=str)
@click.pass_context
def action_scan(ctx: click.Context, uuid: str) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    result = app.client.post(
        f"/scanboxes/{scanbox_id}/mailings/{uuid}/action_requests",
        payload={"action_type": "scan"},
    )
    output.detail(result)


@action_group.command(
    "forward",
    help="Request physical forwarding to a registered forwarding address.",
)
@click.argument("uuid", type=str)
@click.option("--address-id", required=True, type=str)
@click.option("--date", "forward_date", required=True, type=str, help="YYYY-MM-DD")
@click.pass_context
def action_forward(ctx: click.Context, uuid: str, address_id: str, forward_date: str) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    result = app.client.post(
        f"/scanboxes/{scanbox_id}/mailings/{uuid}/action_requests",
        payload={
            "action_type": "forward",
            "forwarding_options": {
                "address_id": address_id,
                "date": forward_date,
            },
        },
    )
    output.detail(result)


@action_group.command("destroy", help="Request permanent destruction of the physical mailing.")
@click.argument("uuid", type=str)
@click.option("--yes", is_flag=True, help="Skip confirmation prompt.")
@click.pass_context
def action_destroy(ctx: click.Context, uuid: str, yes: bool) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    if not yes:
        click.confirm("Permanently destroy this mailing? This cannot be undone.", abort=True)
    result = app.client.post(
        f"/scanboxes/{scanbox_id}/mailings/{uuid}/action_requests",
        payload={"action_type": "destroy"},
    )
    output.detail(result)


@action_group.command("cancel", help="Cancel a previously requested mailing action.")
@click.argument("mailing_uuid", type=str)
@click.argument("action_id", type=str)
@click.pass_context
def action_cancel(ctx: click.Context, mailing_uuid: str, action_id: str) -> None:
    app: AppContext = ctx.obj
    scanbox_id = app.require_scanbox()
    app.client.delete(f"/scanboxes/{scanbox_id}/mailings/{mailing_uuid}/action_requests/{action_id}")
    output.message("Action request cancelled.")
