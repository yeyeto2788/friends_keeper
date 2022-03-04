from unittest import mock

import pytest

from friends_keeper.core import main_core
from friends_keeper.exceptions import ConfigurationError


@mock.patch("friends_keeper.core.get_friend")
@mock.patch("friends_keeper.notifiers.base.get_friend")
@mock.patch("friends_keeper.core.get_today_notifications")
@mock.patch("friends_keeper.core.load_configuration_file")
def test_main_core(
    load_configuration_mocked,
    get_today_notifications,
    base_get_friend_mocked,
    orm_get_friend_mocked,
    normal_dumb_config,
    two_notifications,
    friend_by_index,
):
    base_get_friend_mocked.return_value = friend_by_index
    orm_get_friend_mocked.return_value = friend_by_index
    get_today_notifications.return_value = two_notifications
    load_configuration_mocked.return_value = normal_dumb_config
    main_core(debug_level=0)

    assert True == load_configuration_mocked.called
    assert True == get_today_notifications.called


@mock.patch("friends_keeper.core.get_today_notifications")
@mock.patch("friends_keeper.core.load_configuration_file")
def test_main_core_abnormal1(load_configuration_mocked, get_today_notifications):
    get_today_notifications.return_value = []
    load_configuration_mocked.side_effect = ConfigurationError
    try:
        main_core(debug_level=0)
    except ConfigurationError:
        pass
    else:
        pytest.raises(ConfigurationError)


@mock.patch("friends_keeper.core.NotifierFactory")
@mock.patch("friends_keeper.core.get_today_notifications")
@mock.patch("friends_keeper.core.load_configuration_file")
def test_main_core_abnormal2(
    load_configuration_mocked, get_today_notifications, notifier_factory_mocked, normal_dumb_config, two_notifications
):
    notifier_factory_mocked.get_notifiers.side_effect = NotImplementedError
    get_today_notifications.return_value = two_notifications
    load_configuration_mocked.return_value = normal_dumb_config
    main_core(debug_level=0)
    pytest.raises(NotImplementedError)


@mock.patch("friends_keeper.core.get_today_notifications")
@mock.patch("friends_keeper.core.load_configuration_file")
def test_main_core_abnormal_no_notifications(load_configuration_mocked, get_today_notifications, normal_dumb_config):
    get_today_notifications.return_value = []
    load_configuration_mocked.return_value = normal_dumb_config
    main_core(debug_level=0)

    assert True == load_configuration_mocked.called
    assert True == get_today_notifications.called
