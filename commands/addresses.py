import click

from context import AppContext
from output import output


@click.group("addresses")
def addresses_group() -> None:
    """Manage forwarding addresses."""


@addresses_group.command("register")
@click.option("--firstname", prompt=True, required=True, type=str)
@click.option("--lastname", prompt=True, required=True, type=str)
@click.option("--street", prompt=True, required=True, type=str)
@click.option("--number", prompt=True, required=True, type=str)
@click.option("--zip", "zip_code", prompt=True, required=True, type=str)
@click.option("--city", prompt=True, required=True, type=str)
@click.option("--country-code", prompt=True, required=True, type=str)
@click.option("--company", type=str, default=None)
@click.option("--state", type=str, default=None)
@click.option("--info", type=str, default=None)
@click.pass_context
def register_address(
    ctx: click.Context,
    firstname: str,
    lastname: str,
    street: str,
    number: str,
    zip_code: str,
    city: str,
    country_code: str,
    company: str | None,
    state: str | None,
    info: str | None,
) -> None:
    app: AppContext = ctx.obj
    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "street": street,
        "number": number,
        "zip": zip_code,
        "city": city,
        "country_code": country_code,
        "company": company,
        "state": state,
        "info": info,
    }
    result = app.client.post("/forwarding_addresses", payload=payload)
    output.detail(result)


@addresses_group.command("show")
@click.argument("address_id", type=str)
@click.pass_context
def show_address(ctx: click.Context, address_id: str) -> None:
    app: AppContext = ctx.obj
    result = app.client.get(f"/forwarding_addresses/{address_id}")
    output.detail(result)
