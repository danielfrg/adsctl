import click

from adsctl.__about__ import __version__
from adsctl.cli.utils import create_app
from adsctl.prompt.prompt import print_results, prompt_loop


@click.command()
@click.option(
    "--config-file",
    "-f",
    "config_file_path",
    envvar="ADSCTL_CONFIG",
    help="The path to a custom config file to use [env var: `ADSCTL_CONFIG`]",
)
@click.option(
    "--account",
    "-a",
    "account",
    help="The account to use. Defaults to the current_account in the config file.",
)
@click.option("--customer-id", "-i", "customer_id_opt", help="Google Ads Customer ID.")
@click.option(
    "--output",
    "-o",
    default="table",
    type=click.Choice(["table", "plain", "csv", "csv-files"], case_sensitive=False),
)
@click.option(
    "--command",
    "-c",
    help="Inline command to run. If not provided, will enter interactive mode.",
)
@click.option(
    "--filename",
    "-f",
    "input_file",
    type=click.File("rb"),
    help="File to read query from.",
)
@click.option(
    "--var",
    "-v",
    "variables",
    multiple=True,
    help="Variables to render the query before sending it.",
)
@click.version_option(version=__version__, prog_name="AdsCTL")
@click.pass_context
def main(
    ctx: click.Context,
    config_file_path,
    account,
    customer_id_opt,
    output,
    command,
    input_file,
    variables,
):
    """Interactive GAQL prompt"""

    app = create_app(config_file_path, account=account, customer_id=customer_id_opt)
    app.load_config()
    ctx.obj = app

    variables = dict(v.split("=") for v in variables)

    if command or input_file:
        if input_file is not None:
            command = input_file.read()

        results = app.query(query=command, params=variables)

        if output == "csv-files":
            for table, df in results.items():
                fname = f"{table}.csv"
                df.to_csv(fname, index=False)
        else:
            print_results(results, output=output)
    else:
        prompt_loop(app, output=output, params=variables)


if __name__ == "__main__":
    main()
