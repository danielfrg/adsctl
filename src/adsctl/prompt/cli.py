import os
import sys

import click
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf.json_format import MessageToDict
from prettytable import PrettyTable
from prompt_toolkit import PromptSession

from adsctl.__about__ import __version__
from adsctl.cli.app import Application
from adsctl.config.config_file import ConfigFile
from adsctl.utils.fs import Path
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

    used_config_file = Path()
    app = Application(
        config_file=ConfigFile()
    )

    if config_file_path:
        used_config_file = Path(config_file_path).resolve()
        if not used_config_file.is_file():
            click.echo(f'The selected config file `{str(config_file_path)}` does not exist.')
            sys.exit(1)
        app.config_file = ConfigFile(used_config_file)
    elif not app.config_file.path.is_file():
        click.echo('No config file found, creating one with default settings now...')

        try:
            app.config_file.restore()
            click.echo(f'Default config file created at: {app.config_file.path}')
            click.echo(f'Edit that file to include your Google Ads credentials.')
            sys.exit(0)
        except OSError:  # no cov
            click.echo(
                f'Unable to create config file located at `{str(app.config_file.path)}`. Please check your permissions.',
                err=True
            )

    ctx.obj = app

    click.echo(f"Using config: ${app.config_file.path}")
    app.config_file.load()
    settings = app.config_file.model

    google_ads_config = {
        "developer_token": settings.developer_token,
        "client_id": settings.oauth.client_id,
        "client_secret": settings.oauth.client_secret,
        "refresh_token": settings.oauth.refresh_token,
        "use_proto_plus": False
    }

    customer_id = settings.customer_id
    if customer_id_opt is not None:
        customer_id = customer_id_opt
    customer_id = customer_id.replace("-", "")
    app.customer_id = customer_id

    print(google_ads_config)

    google_ads_client = get_google_ads_client(google_ads_config)
    app.client = google_ads_client
    prompt(google_ads_client, customer_id, plain=plain)


def prompt(client, customer_id, plain=False):
    ga_service = client.get_service("GoogleAdsService")
    session = PromptSession()

    ignoreFields = ()
    while True:
        try:
            query = session.prompt(">>> ").strip()

            if not query:
                continue

            if query == "exit":
                sys.exit(0)

            stream = ga_service.search_stream(customer_id=customer_id, query=query)

            tables = {}

            count = 0
            for batch in stream:
                for row in batch.results:
                    if not plain:
                        try:
                            if count == 0:
                                # Empty line to give space between queries
                                print("")

                            count += 1
                            if hasattr(row, "_pb"):
                                results_dict = MessageToDict(row._pb)
                            else:
                                results_dict = MessageToDict(row)

                            for table, values in results_dict.items():
                                if table not in tables:
                                    tables[table] = PrettyTable()
                                tables[table].add_row(
                                    [
                                        value
                                        for key, value in values.items()
                                        if key not in ignoreFields
                                    ]
                                )
                        except Exception as e:
                            count += 1
                            print(row)
                    else:
                        count += 1
                        print(row)

            for table, prettyTable in tables.items():
                print(prettyTable)

            if count == 0:
                print("No results found")

        except GoogleAdsException as ex:
            # Continue on query errors
            print(ex)
        except KeyboardInterrupt:
            pass
        except EOFError:
            # Control-D pressed
            sys.exit()


if __name__ == "__main__":
    main()
