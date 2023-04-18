import os

import pytest


@pytest.fixture(scope="session")
def customer_id():
    return os.environ.get("GOOGLE_ADS_CUSTOMER_ID")


def pytest_addoption(parser):
    parser.addoption(
        "--ads-api",
        action="store_true",
        dest="adsapi",
        default=False,
        help="Enable the Ads API tests",
    )


def pytest_configure(config):
    if not config.option.adsapi:
        setattr(config.option, "markexpr", "not adsapi")
