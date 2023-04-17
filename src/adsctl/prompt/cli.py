import click

from adsctl.__about__ import __version__
from adsctl.cli.utils import load_config
from adsctl.prompt.prompt import prompt
from adsctl.utils.googleads import get_client as get_google_ads_client


@click.command()
@click.option(
    "--config-file",
    "-f",
    "config_file_path",
    envvar="ADSCTL_CONFIG",
    help="The path to a custom config file to use [env var: `ADSCTL_CONFIG`]",
)
@click.option("--customer-id", "-c", "customer_id_opt", help="Google Ads Customer ID.")
@click.option("--plain", "-p", is_flag=True, help="Do not print tables.")
@click.version_option(version=__version__, prog_name="AdsCTL")
@click.pass_context
def main(ctx: click.Context, config_file_path, customer_id_opt, plain):
    """Interactive GAQL prompt."""

    app = load_config(config_file_path)

    click.echo(f"Using config: ${app.config_file.path}")
    app.config_file.load()
    settings = app.config_file.model

    google_ads_config = {
        "developer_token": settings.developer_token,
        "client_id": settings.oauth.client_id,
        "client_secret": settings.oauth.client_secret,
        "refresh_token": settings.oauth.refresh_token,
        "use_proto_plus": False,
    }

    customer_id = settings.customer_id
    if customer_id_opt is not None:
        customer_id = customer_id_opt
    customer_id = customer_id.replace("-", "")
    app.customer_id = customer_id

    print(google_ads_config)

    google_ads_client = get_google_ads_client(google_ads_config)
    app.client = google_ads_client

    ctx.obj = app
    prompt(google_ads_client, customer_id, plain=plain)


if __name__ == "__main__":
    main()
