import click

from adsctl.application import Application
from adsctl.cli.edit.campaign import campaign


@click.group()
@click.pass_obj
def edit(app: Application):
    try:
        app.load_config()
    except Exception as e:
        click.echo(f"Error loading config: {e}")


edit.add_command(campaign)
