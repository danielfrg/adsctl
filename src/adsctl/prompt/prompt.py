import sys

from google.ads.googleads.errors import GoogleAdsException
from google.protobuf.json_format import MessageToDict
from prettytable import PrettyTable
from prompt_toolkit import PromptSession


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
                        except Exception:
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
