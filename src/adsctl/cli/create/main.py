import click

from adsctl.application import Application
from adsctl.cli.create.asset import asset


@click.group()
@click.pass_obj
def create(app: Application):
    try:
        app.load_config()
    except Exception as e:
        click.echo(f"Error loading config: {e}")


create.add_command(asset)
