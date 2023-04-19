import click

from adsctl.__about__ import __version__
from adsctl.cli.utils import create_app
from adsctl.prompt.prompt import make_query, print_results, prompt_loop


@click.command()
@click.option(
    "--config-file",
    "-f",
    "config_file_path",
    envvar="ADSCTL_CONFIG",
    help="The path to a custom config file to use [env var: `ADSCTL_CONFIG`]",
)
@click.option("--customer-id", "-c", "customer_id_opt", help="Google Ads Customer ID.")
@click.option(
    "--output",
    "-o",
    default="table",
    type=click.Choice(["table", "plain", "csv", "csv-files"], case_sensitive=False),
)
@click.option(
    "--command",
    "-c",
)
@click.option("--filename", "-f", "input_file", type=click.File("rb"))
@click.version_option(version=__version__, prog_name="AdsCTL")
@click.pass_context
def main(
    ctx: click.Context, config_file_path, customer_id_opt, output, command, input_file
):
    """Interactive GAQL prompt."""

    app = create_app(config_file_path, customer_id=customer_id_opt)
    # click.echo(f"Using config: {app.config_file.path}")

    app.create_client()

    ctx.obj = app
    ga_service = app.client.get_service("GoogleAdsService")

    if command or input_file:
        if input_file is not None:
            command = input_file.read()

        results = make_query(ga_service, app.customer_id, command, output=output)
        if output == "csv-files":
            for table, df in results.items():
                fname = f"{table}.csv"
                df.to_csv(fname, index=False)
        else:
            print_results(results, output=output)
    else:
        prompt_loop(ga_service, app.customer_id, output=output)


if __name__ == "__main__":
    main()
