import os

import click
from click_shell import shell
from dotenv import load_dotenv

from client import DropscanClient
from commands.actions import action_group
from commands.addresses import addresses_group
from commands.mailings import mailings_group
from commands.recipients import recipients_group
from commands.scanboxes import scanbox_group
from context import AppContext


load_dotenv()


@shell(prompt="dropscan> ", intro="Dropscan CLI")
@click.pass_context
def cli(ctx: click.Context) -> None:
    api_key = os.getenv("DROPSCAN_API_KEY")
    if not api_key:
        raise click.ClickException("Missing DROPSCAN_API_KEY in environment.")

    base_url = os.getenv("DROPSCAN_API_BASE_URL", "https://api.dropscan.de/v1")
    ctx.obj = AppContext(client=DropscanClient(api_key=api_key, base_url=base_url))


cli.add_command(scanbox_group)
cli.add_command(mailings_group)
cli.add_command(action_group)
cli.add_command(recipients_group)
cli.add_command(addresses_group)


if __name__ == "__main__":
    cli()
