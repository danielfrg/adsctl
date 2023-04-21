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
    assert app.account.login_customer_id == "7777777777"


def test_config_1_account_2(templates):
    app = adsctl.Application(templates / "config_1.toml", account="second")

    assert app is not None
    assert app.config_file_path == templates / "config_1.toml"
    assert app.config_file is not None
    assert app.config_file.account_name == "second"

    # On the file we still have "default" but its not used on the App
    assert app.config.current_account == "default"
    assert app.account.developer_token == "BBBBBBBBBB"
    assert app.account.customer_id == "9087654321"
    assert app.account.login_customer_id == ""


def test_config_inv_customer_id(templates):
    with pytest.raises(ValidationError):
        app = adsctl.Application(templates / "config_invalid_id.toml")
        assert app.account.customer_id


def test_custom_customer_id(templates):
    app = adsctl.Application(templates / "config_1.toml", customer_id="555-555-5555")

    assert app.customer_id == "5555555555"
