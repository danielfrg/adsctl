import sys
from typing import Union

import click
from google.ads.googleads.errors import GoogleAdsException
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter, ThreadedCompleter
from prompt_toolkit.history import FileHistory
from tabulate import tabulate

from adsctl.application import Application
from adsctl.prompt.completer import MyCustomCompleter
from adsctl.prompt.key_bindings import adsctl_bindings


def prompt_loop(app: Application, output="table", params: Union[dict, None] = None):
    if app.config_file_path is None:
        my_history = None
    else:
        history_file = app.config_file_path.parent / "history.txt"
        my_history = FileHistory(str(history_file))

    key_bindings = adsctl_bindings()
    ThreadedCompleter(FuzzyCompleter(MyCustomCompleter()))
    session = PromptSession(
        history=my_history,
        # completer=completer,
        # complete_while_typing=True,
        key_bindings=key_bindings,
        multiline=True,
    )

    while True:
        try:
            query = session.prompt(">>> ").strip()

            if not query:
                continue

            if query == "exit":
                sys.exit(0)

            results = app.query(query=query, params=params)

            print(results)

            if output == "plain":
                results = []
                for batch in results:
                    for row in batch.results:
                        results.append(row)
            elif output in ("table", "csv", "csv-files"):
                for table, df in results.items():
                    results[table] = df

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
                click.echo(df.to_csv(index=False))
        for _, df in results.items():
            if len(df) > 0:
                click.echo(df.to_csv(index=False))
                click.echo(df.to_csv(index=False))
