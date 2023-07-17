import click

from adsctl.application import Application
from adsctl.cli.get.campaign import campaign


@click.group()
@click.pass_obj
def get(app: Application):
    try:
        app.load_config()
    except Exception as e:
        click.echo(f"Error loading config: {e}")


get.add_command(campaign)
