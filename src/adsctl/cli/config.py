import argparse
import hashlib
import os
import re
import socket
import sys
from urllib.parse import unquote

import click
# If using Web flow, the redirect URL must match exactly what’s configured in GCP for
# the OAuth client.  If using Desktop flow, the redirect must be a localhost URL and
# is not explicitly set in GCP.
from google_auth_oauthlib.flow import Flow

_SCOPE = "https://www.googleapis.com/auth/adwords"
_SERVER = "127.0.0.1"
_PORT = 8080
_REDIRECT_URI = f"http://{_SERVER}:{_PORT}"


@click.group()
@click.pass_obj
def config(app):
    """View and manage configuration
    """

@config.command()
@click.pass_obj
def info(app):
    """Show information about the config."""
    click.echo(f'Config file: {app.config_file.path}')


@config.command()
@click.pass_obj
def explore(app):
    """Open the config location in your file manager."""
    click.launch(str(app.config_file.path), locate=True)


@config.command()
@click.pass_obj
def show(app):
    """Show the contents of the config file."""
    if not app.config_file.path.is_file():  # no cov
        app.display_critical('No config file found! Try: `adsctl config restore`.')
    else:
        click.echo(app.config_file.read())


