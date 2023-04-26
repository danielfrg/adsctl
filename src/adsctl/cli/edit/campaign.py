import sys

import click

import adsctl.api.campaign.budget as budget_api
import adsctl.api.campaign.main as campaign_api
import adsctl.api.campaign.status as status_api
from adsctl.application import Application


@click.group()
@click.option("--campaign-id", "-i", required=True, help="Campaign ID.")
@click.pass_obj
def campaign(app: Application, campaign_id):
    app.params["campaign_id"] = campaign_id


@campaign.command("status")
@click.argument("status", type=click.Choice(["enabled", "paused"]))
@click.pass_obj
def status(app: Application, status):
    """Set campaign budget."""
    campaign_id = app.params["campaign_id"]
    campaign_rn = campaign_api.get_rn(campaign_id, app=app)

    if campaign_rn is None:
        click.echo(f"Campaign with id '{campaign_id}' not found.")
        sys.exit(1)

    r = status_api.mutate(status, campaign_id=campaign_id, app=app)
    click.echo(f"Campaign updated: {r.results[0].resource_name}")


@campaign.command("budget")
@click.argument("budget", type=float)
@click.pass_obj
def budget_(app: Application, budget):
    """Set campaign budget."""
    campaign_id = app.params["campaign_id"]
    budget_rn = budget_api.get_rn(campaign_id=campaign_id, app=app)

    if budget_rn is None:
        click.echo(f"Budget not found for campaign {campaign_id}")
        sys.exit(1)

    r = budget_api.mutate(budget, resource_name=budget_rn, app=app)
    click.echo(f"Budget updated: {r.results[0].resource_name}")
