import logging
import sys

import click

from adsctl.__about__ import __version__
from adsctl.cli.app import Application
from adsctl.cli.auth import auth
from adsctl.cli.config import config
from adsctl.cli.edit.edit import edit
from adsctl.config.config_file import ConfigFile
from adsctl.utils.fs import Path

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s - %(levelname)s] %(message).5000s"
)
logging.getLogger("google.ads.googleads.client").setLevel(logging.INFO)


@click.group()
@click.option(
    "--config-file",
    "-f",
    "config_file_path",
    envvar="ADSCTL_CONFIG",
    help="The path to a custom config file to use [env var: `ADSCTL_CONFIG`]",
)
@click.version_option(version=__version__, prog_name="AdsCTL")
@click.pass_context
def main(ctx: click.Context, config_file_path):
    """Google Ads CLI."""

    used_config_file = Path()
    app = Application(
        config_file=ConfigFile()
    )

    if config_file_path:
        used_config_file = Path(config_file_path).resolve()
        if not used_config_file.is_file():
            click.echo(f'The selected config file `{str(config_file_path)}` does not exist.')
            sys.exit(1)
        app.config_file = ConfigFile(used_config_file)
    elif not app.config_file.path.is_file():
        click.echo('No config file found, creating one with default settings now...')

        try:
            app.config_file.restore()
            click.echo(f'Default config file created at: {app.config_file.path}')
            click.echo(f'Edit that file to include your Google Ads credentials.')
            sys.exit(0)
        except OSError:  # no cov
            click.echo(
                f'Unable to create config file located at `{str(app.config_file.path)}`. Please check your permissions.',
                err=True
            )

    ctx.obj = app


main.add_command(auth)
main.add_command(edit)
main.add_command(config)


if __name__ == "__main__":
    main()
