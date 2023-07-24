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
    app.create_client()

    query.format(status="ENABLED")
    tables = app.query(query)

    table = []
    for _index, row in tables["campaign"].iterrows():
        print(row)
        table.append([row["name"], row.status, row.id])

    headers = ["Name", "Status", "Id"]

    click.echo(tabulate(table, headers=headers))
    return None
