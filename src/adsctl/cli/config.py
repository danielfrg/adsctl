import sys

import click

from adsctl.config.config_file import ConfigFile


@click.group()
@click.pass_obj
def config(app):
    """View and manage configuration"""


@config.command()
@click.pass_obj
def init(app):
    """Create a base config file"""
    # TODO: Add force flag to overwrite existing config file

    if not app.config_file.path.is_file():
        click.echo("Config file not found. Creating one with default settings now...")

        try:
            app.config_file.restore()
            click.echo(f"Default config file created at: {app.config_file.path}")
            click.echo("Edit that file to include your Google Ads credentials.")
            sys.exit(0)
        except OSError:  # no cov
            click.echo(
                f"Unable to create config file located at"
                f"`{str(app.config_file.path)}`. Please check your permissions.",
                err=True,
            )
    else:
        click.echo(
            f"Config file already exists at: {app.config_file.path}.\n"
            "If you want to overwrite it, delete it first."
        )


@config.command()
@click.pass_obj
def explore(app):
    """Open the config location in your file manager"""
    try:
        click.launch(str(app.config_file.path), locate=True)
    except Exception:
        click.launch(str(ConfigFile.get_default_location().parent), locate=True)


@config.command()
@click.pass_obj
def view(app):
    """Show the contents of the config file"""
    click.echo(f"# Config file: {app.config_file.path}\n")

    if not app.config_file.path.is_file():  # no cov
        app.display_critical("No config file found! Try: `adsctl config restore`.")
    else:
        click.echo(app.config_file.read())
