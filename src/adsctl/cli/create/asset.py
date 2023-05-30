import click

import adsctl.api.asset.image as image_asset_api
from adsctl.application import Application


@click.group()
@click.pass_obj
def asset(app: Application):
    pass


@asset.command("image")
@click.argument("asset_name")
@click.argument("filepath", type=click.Path(exists=True))
@click.pass_obj
def image(app: Application, asset_name, filepath):
    """Set campaign budget."""

    image_asset_api.create(filepath, asset_name, app)
