import logging
import os

import click
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from adsctl.cli.auth import auth
from adsctl.cli.edit.edit import edit

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s - %(levelname)s] %(message).5000s"
)
logging.getLogger("google.ads.googleads.client").setLevel(logging.INFO)


@click.group()
@click.option(
    "--config",
    "-f",
    default=os.path.join(os.path.expanduser("~"), "google-ads.yaml"),
    type=click.Path(exists=True),
    help="Path to the Google Ads credentials file.",
)
@click.pass_context
def main(ctx, config):
    """Google Ads CLI"""
    ctx.obj = Context(config)


main.add_command(auth)
main.add_command(edit)


class Context:
    def __init__(self, config_file):
        self.config_file = config_file
        self.client = None


if __name__ == "__main__":
    main()
