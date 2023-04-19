import logging

import click

from adsctl.__about__ import __version__
from adsctl.cli.auth import auth
from adsctl.cli.config import config
from adsctl.cli.edit.main import edit
from adsctl.cli.utils import create_app


@click.group()
@click.option(
    "--config-file",
    "-f",
    "config_file_path",
    envvar="ADSCTL_CONFIG",
    help="The path to a custom config file to use [env var: `ADSCTL_CONFIG`]",
)
@click.option(
    "-l",
    "enable_logging",
    is_flag=True,
    show_default=True,
    default=False,
    help="Enable Google Ads Python logging",
)
@click.version_option(version=__version__, prog_name="AdsCtl")
@click.pass_context
def main(ctx: click.Context, config_file_path, enable_logging):
    """Google Ads CLI."""

    if enable_logging:
        logging.basicConfig(
            level=logging.INFO, format="[%(asctime)s - %(levelname)s] %(message).5000s"
        )
        logging.getLogger("google.ads.googleads.client").setLevel(logging.INFO)

    app = create_app(config_file_path)
    ctx.obj = app


main.add_command(auth)
main.add_command(edit)
main.add_command(config)


if __name__ == "__main__":
    main()
