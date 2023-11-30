import click
from tabulate import tabulate

from adsctl.application import Application

query = """
SELECT ad_group.name, ad_group.id, ad_group.status
FROM ad_group
"""


@click.command()
@click.pass_obj
def ad_group(app: Application):
    app.create_client()

    # query.format(status="ENABLED")
    tables = app.query(query)

    table = []
    for _, row in tables["adGroup"].iterrows():
        table.append([row["name"], row.status, row.id])

    headers = ["Name", "Status", "Id"]
    click.echo(tabulate(table, headers=headers))
    return None
