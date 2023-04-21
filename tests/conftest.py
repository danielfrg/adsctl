import os

import pytest

from adsctl.utils.fs import Path


@pytest.fixture(scope="session")
def customer_id():
    return os.environ.get("GOOGLE_ADS_CUSTOMER_ID")


@pytest.fixture()
def templates(request):
    test_dir = os.path.dirname(request.module.__file__)
    return Path(test_dir) / "templates"


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
        config.option.markexpr = "not adsapi"
