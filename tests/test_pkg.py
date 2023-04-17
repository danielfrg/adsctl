import pytest

from adsctl import __about__ as ads_about

pytestmark = [pytest.mark.pkg]


def test_import():
    assert ads_about.__version__ is not None
    assert ads_about.__version__ != "0.0.0"
    assert len(ads_about.__version__) > 0
