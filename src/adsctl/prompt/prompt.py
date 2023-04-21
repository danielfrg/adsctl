import sys

import click
from google.ads.googleads.errors import GoogleAdsException
from prompt_toolkit import PromptSession
from tabulate import tabulate

from adsctl.application import Application
from adsctl.parse import parseStream


def prompt_loop(app: Application, output="table", params: dict | None = None):
    session = PromptSession()

    while True:
        try:
            query = session.prompt(">>> ").strip()

            if not query:
                continue

            if query == "exit":
                sys.exit(0)

            results = app.query(query=query, params=params)
            # results = make_query(ga_service, customer_id, query, output=output)

            if results is None:
                continue

            print_results(results, output=output)

        except GoogleAdsException as ex:
            # Continue on query errors
            click.echo(ex)
        except KeyboardInterrupt:
            pass
        except EOFError:
            # Control-D pressed
            sys.exit()


def make_query(
    app: Application, query, output="table", params: dict | None = None
) -> None | list | dict:
    results = None
    stream = app.search_stream(query, params=params)

    if output == "plain":
        results = []
        for batch in stream:
            for row in batch.results:
                results.append(row)
    elif output in ("table", "csv", "csv-files"):
        results = {}
        tables = parseStream(stream, pandas=True)

        for table, df in tables.items():
            results[table] = df

    return results


def print_results(results, output="table"):
    if output == "plain":
        if len(results) == 0:
            click.echo("No results found")
        for row in results:
            click.echo(row)
    elif output == "table":
        for table, df in results.items():
            click.echo(f"Table: {table}")
            if len(df) == 0:
                click.echo("No results found")
            else:
                click.echo(tabulate(df, headers="keys", tablefmt="psql"))
    elif output == "csv":
        for _, df in results.items():
            if len(df) > 0:
                click.echo(df.to_csv(index=False))
