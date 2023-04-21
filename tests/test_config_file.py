import pytest
from pydantic import ValidationError

import adsctl
from adsctl.config.config_file import ConfigFile


def test_config_default():
    app = adsctl.Application(load_config=False)
    assert app is not None
    assert app.config_file_path == ConfigFile.get_default_location()
    assert app.config_file is not None


def test_config_1(templates):
    app = adsctl.Application(templates / "config_1.toml")

    assert app is not None
    assert app.config_file_path == templates / "config_1.toml"
    assert app.config_file is not None
    assert app.config_file.account_name is None  # No account specified

    assert app.config.current_account == "default"
    assert app.account.developer_token == "AAAAAAAAAA"
    assert app.account.customer_id == "1234567890"


def test_config_inv_customer_id(templates):

    with pytest.raises(ValidationError):
        app = adsctl.Application(templates / "config_invalid_id.toml")
        assert app.account.customer_id
