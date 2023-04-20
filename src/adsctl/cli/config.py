import sys

import click

from adsctl.application import Application
from adsctl.cli.utils import replace_field
from adsctl.config.config_file import ConfigFile


@click.group()
@click.pass_obj
def config(app: Application):
    """View and manage configuration"""


@config.command()
@click.pass_obj
def init(app: Application):
    """Create a base config file"""
    # TODO: Add force flag to overwrite existing config file

    if not app.config_file.path.is_file():
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


@config.command("get-account")
@click.pass_obj
def get_account(app: Application):
    """Display the current account"""
    app.load_config()

    account_name = app.config.current_account
    click.echo(account_name)


@config.command("set-account")
@click.argument("account_name")
@click.pass_obj
def set_account(app: Application, account_name):
    """Set the current account"""
    app.load_config()

    if account_name in app.config.accounts.keys():
        new_content = replace_field(
            app.config_file.read(),
            "current_account",
            app.config.current_account,
            account_name,
        )
        app.config_file.path.write(new_content)
        click.echo(f"Current account set to: {account_name}")
    else:
        click.echo(f"Account `{account_name}` does not exist in the config file.")


@config.command()
@click.pass_obj
def explore(app: Application):
    """Open the config location in your file manager"""
    try:
        click.launch(str(app.config_file.path), locate=True)
    except Exception:
        click.launch(str(ConfigFile.get_default_location().parent), locate=True)


@config.command()
@click.pass_obj
def view(app: Application):
    """Show the contents of the config file"""
    click.echo(f"# Config file: {app.config_file.path}\n")

    if not app.config_file.path.is_file():  # no cov
        app.display_critical("No config file found! Try: `adsctl config restore`.")
    else:
        click.echo(app.config_file.read())
