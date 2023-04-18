import sys

import click
from google.ads.googleads.errors import GoogleAdsException
from prompt_toolkit import PromptSession
from tabulate import tabulate

from adsctl.parse import parseStream


def prompt(client, customer_id, plain=False):
    ga_service = client.get_service("GoogleAdsService")
    session = PromptSession()

    while True:
        try:
            query = session.prompt(">>> ").strip()

            if not query:
                continue

            if query == "exit":
                sys.exit(0)

            stream = ga_service.search_stream(customer_id=customer_id, query=query)

            count = 0
            if plain:
                for batch in stream:
                    for row in batch.results:
                        count += 1
                        click.echo(row)
            else:
                tables = parseStream(stream)

                for table, df in tables.items():
                    click.echo(table)
                    click.echo(tabulate(df, headers="keys", tablefmt="psql"))

            if count == 0:
                click.echo("No results found")

        except GoogleAdsException as ex:
            # Continue on query errors
            click.echo(ex)
        except KeyboardInterrupt:
            pass
        except EOFError:
            # Control-D pressed
            sys.exit()
