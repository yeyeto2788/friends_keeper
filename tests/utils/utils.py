from unittest import mock

import pytest

from friends_keeper.exceptions import ConfigurationError
from friends_keeper.utils import load_configuration_file


@mock.patch("friends_keeper.utils.yaml")
@mock.patch("friends_keeper.utils.check_config")
def test_load_configuration(check_config_mocked, safe_load_mocked):
    dump_config = {"all_ok": True}
    safe_load_mocked.safe_load.return_value = dump_config
    check_config_mocked.return_value = True
    result = load_configuration_file()
    assert result == dump_config


@mock.patch("friends_keeper.utils.yaml")
@mock.patch("friends_keeper.utils.check_config")
def test_load_configuration_abnormal(check_config_mocked, safe_load_mocked):
    dump_config = {"all_ok": True}
    safe_load_mocked.safe_load.return_value = dump_config
    check_config_mocked.return_value = False
    pytest.raises(ConfigurationError)
