import sys

import click
from google.ads.googleads.errors import GoogleAdsException
from prompt_toolkit import PromptSession
from tabulate import tabulate

from adsctl.parse import parseStream


def prompt(client, customer_id, output="table"):
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

            if output == "plain":
                count = 0
                for batch in stream:
                    for row in batch.results:
                        count += 1
                        click.echo(row)
                if count == 0:
                    click.echo("No results found")
            else:
                use_pandas = output == "table"
                tables = parseStream(stream, pandas=use_pandas)

                for table, df in tables.items():
                    click.echo(f"Table: {table}")
                    if use_pandas:
                        if len(df) == 0:
                            click.echo("No results found")
                        click.echo(tabulate(df, headers="keys", tablefmt="psql"))
                    else:
                        click.echo(df)

        except GoogleAdsException as ex:
            # Continue on query errors
            click.echo(ex)
        except KeyboardInterrupt:
            pass
        except EOFError:
            # Control-D pressed
            sys.exit()
