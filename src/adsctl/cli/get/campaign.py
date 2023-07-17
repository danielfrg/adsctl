import click
from tabulate import tabulate

from adsctl.application import Application

query = """
SELECT campaign.name, campaign.id, campaign.status
FROM campaign
WHERE campaign.status IN ('ENABLED', 'PAUSED')
"""


@click.command()
@click.pass_obj
def campaign(app: Application):
    client = app.create_client()

    status_enums = client.enums.CampaignStatusEnum

    status_map = {
        status_enums.ENABLED: "Enabled",
        status_enums.PAUSED: "Paused",
        status_enums.REMOVED: "Removed",
    }

    query.format(status="ENABLED")
    response = app.search(query, client)

    table = []
    for row in response:
        table.append(
            [row.campaign.name, status_map[row.campaign.status], row.campaign.id]
        )

    headers = ["Name", "Status", "Id"]

    click.echo(tabulate(table, headers=headers))
    return None
