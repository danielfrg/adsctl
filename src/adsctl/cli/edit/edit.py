import sys

import click
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.auth.exceptions import RefreshError

import adsctl.cli.edit.campaign.budget as budget_


@click.option("--customer-id", "-c", required=True, help="Google Ads Customer ID.")
@click.option("--version", "-v", default="v13", help="Google Ads Customer ID.")
@click.group()
@click.pass_obj
def edit(obj, version, customer_id):
    try:
        # GoogleAdsClient will read the google-ads.yaml configuration file in the
        # home directory if none is specified.
        googleads_client = GoogleAdsClient.load_from_storage(
            obj.config_file, version=version
        )
        obj.client = googleads_client
        obj.customer_id = customer_id
    except RefreshError as ex:
        click.echo(
            "Token has been expired or revoked. \nTry re-running the "
            "authentication command:\n\n    adsctl auth"
        )
        sys.exit(1)
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


@edit.group()
@click.option("--campaign-id", "-i", required=True, help="Campaign ID.")
@click.pass_obj
def campaign(obj, campaign_id):
    obj.campaign_id = campaign_id


@campaign.command("budget")
@click.argument("budget", type=float)
@click.pass_obj
def budget_fn(obj, budget):
    """Set campaign budget."""
    budget_rn = budget_.get_rn(obj.client, obj.customer_id, obj.campaign_id)

    if budget_rn is None:
        click.echo(f"Budget not found for campaign {obj.campaign_id}")
        sys.exit(1)

    r = budget_.mutate(obj.client, obj.customer_id, budget_rn, budget)
    click.echo(f"Budget updated: {r.results[0].resource_name}")
