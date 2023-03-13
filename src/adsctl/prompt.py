import json
import os
import sys

import click
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import json_format
from prettytable import PrettyTable
from prompt_toolkit import PromptSession


@click.command()
@click.option(
    "--config",
    "-f",
    default=os.path.join(os.path.expanduser("~"), "google-ads.yaml"),
    type=click.Path(exists=True),
    help="Path to the Google Ads credentials file.",
)
@click.option("--customer-id", "-c", required=True, help="Google Ads Customer ID.")
def main(config, customer_id):
    """Simple program that greets NAME for a total of COUNT times."""

    try:
        # GoogleAdsClient will read the google-ads.yaml configuration file in the
        # home directory if none is specified.
        googleads_client = GoogleAdsClient.load_from_storage(config, version="v12")

        prompt(googleads_client, customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)


def prompt(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")
    session = PromptSession()

    ignoreFields = ("resourceName",)

    while True:
        try:
            query = session.prompt(">>> ")

            stream = ga_service.search_stream(customer_id=customer_id, query=query)

            tables = {}

            for batch in stream:
                for row in batch.results:
                    json_str = json_format.MessageToJson(row)
                    d = json.loads(json_str)

                    for table, values in d.items():
                        if table not in tables:
                            tables[table] = PrettyTable()
                            tables[table].field_names = [
                                key for key in values.keys() if key not in ignoreFields
                            ]
                        else:
                            tables[table].add_row(
                                [
                                    value
                                    for key, value in values.items()
                                    if key not in ignoreFields
                                ]
                            )

            for table, prettyTable in tables.items():
                print(prettyTable)

        except KeyboardInterrupt:
            pass
        except EOFError:
            sys.exit()


if __name__ == "__main__":
    main()
