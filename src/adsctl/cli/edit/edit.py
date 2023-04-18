import sys

import click

import adsctl.api.campaign.budget as budget_api
from adsctl.app import Application


@click.group()
def edit():
    pass


@edit.group()
@click.option("--campaign-id", "-i", required=True, help="Campaign ID.")
@click.pass_obj
def campaign(obj, campaign_id):
    obj.params["campaign_id"] = campaign_id


@campaign.command("budget")
@click.argument("budget", type=float)
@click.pass_obj
def budget_(obj: Application, budget):
    """Set campaign budget."""
    obj.create_client()

    campaign_id = obj.params["campaign_id"]
    budget_rn = budget_api.get_rn(campaign_id, app=obj)

    if budget_rn is None:
        click.echo(f"Budget not found for campaign {campaign_id}")
        sys.exit(1)

    r = budget_api.mutate(budget_rn, budget, app=obj)
    click.echo(f"Budget updated: {r.results[0].resource_name}")
