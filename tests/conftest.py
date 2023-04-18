import os

import pytest


@pytest.fixture(scope="session")
def customer_id():
    return os.environ.get("GOOGLE_ADS_CUSTOMER_ID")
