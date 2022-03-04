from unittest import mock

import pytest

from pytest import fail

from friends_keeper.constants import DEFAULT_CONFIGURATION
from friends_keeper.notifiers.base import BaseNotifier


def test_base_notifier_instantiation():
    try:
        BaseNotifier({})
    except TypeError:
        pytest.raises(TypeError)


def test_base_notifier_title_default():
    title = "Loco TITLE"
    configuration = DEFAULT_CONFIGURATION
    notifier = BaseNotifier
    notifier.configuration = {}
    notifier.__init__(notifier, configuration=configuration)
    assert notifier.title != title


def test_base_notifier_title():
    title = "Loco TITLE"
    configuration = DEFAULT_CONFIGURATION
    configuration["notifications"]["title"] = title
    notifier = BaseNotifier
    notifier.configuration = {}
    notifier.__init__(notifier, configuration=configuration)
    assert notifier.title == title


def test_base_notifier_title_empty():
    configuration = DEFAULT_CONFIGURATION
    configuration["notifications"]["title"] = ""
    notifier = BaseNotifier
    notifier.configuration = {}
    notifier.__init__(notifier, configuration=configuration)
    assert notifier.title == "Friends keeper notification"


@mock.patch("friends_keeper.notifiers.base.get_friend")
def test_build_notification_message(get_friend_mock, two_notifications, friend_by_index):
    get_friend_mock.return_value = friend_by_index
    notifier = BaseNotifier
    notifier.__init__(notifier, configuration=DEFAULT_CONFIGURATION)
    result = notifier.build_notification_message(notifier, notifications=two_notifications)
    assert True == get_friend_mock.called
    assert friend_by_index.nickname in result


@mock.patch("friends_keeper.notifiers.base.get_friend")
def test_build_notification_message_from_configuration(get_friend_mock, two_notifications, friend_by_index):
    configuration = DEFAULT_CONFIGURATION
    configuration["notifications"]["message"] = "Test {action} with a {friend_name}"
    get_friend_mock.return_value = friend_by_index
    notifier = BaseNotifier
    notifier.__init__(notifier, configuration=configuration)
    result = notifier.build_notification_message(notifier, notifications=two_notifications)
    assert True == get_friend_mock.called
    assert friend_by_index.nickname in result


def test_base_notifier_notify():
    notifier = BaseNotifier
    notifier.__init__(notifier, configuration=DEFAULT_CONFIGURATION)
    result = notifier.notify(notifier, message="")
    assert result == None
