import click

from adsctl.__about__ import __version__
from adsctl.cli.utils import create_app
from adsctl.client import get_client as get_google_ads_client
from adsctl.prompt.prompt import prompt


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
    app = create_app(config_file_path, customer_id=customer_id_opt)
    click.echo(f"Using config: {app.config_file.path}")

    app.create_client()

    ctx.obj = app
    prompt(app.client, app.customer_id, plain=plain)


if __name__ == "__main__":
    main()
