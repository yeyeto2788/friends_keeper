import json

from unittest import mock

import pytest

from gotify import GotifyError
from gotify import gotify

from friends_keeper.constants import DEFAULT_CONFIGURATION
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.notifiers.gotify import GotifyNotifier


def test_gotify_notifier_initialization_abnormal():
    try:
        GotifyNotifier(configuration=DEFAULT_CONFIGURATION)
    except ConfigurationError:
        pytest.raises(ConfigurationError)


def test_gotify_notifier_initialization():
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["gotify"] = dict()
    configuration["notifiers"]["gotify"]["app_token"] = "loco_token_that_does_not_work"
    configuration["notifiers"]["gotify"]["url"] = "https://loco_url_that_does_not_work.com"
    notifier = GotifyNotifier(configuration=configuration)
    assert notifier.title == "Friends keeper notification"


def test_gotify_notifier_initialization_missing_url():
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["gotify"] = dict()
    configuration["notifiers"]["gotify"]["app_token"] = "loco_token_that_does_not_work"
    try:
        GotifyNotifier(configuration=configuration)
    except ConfigurationError as exec_error:
        pytest.raises(ConfigurationError)
        assert str(exec_error) == "Gotify URL missing in configuration."


def test_gotify_notifier_initialization_missing_token():
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["gotify"] = dict()
    configuration["notifiers"]["gotify"]["url"] = "https://loco_url_that_does_not_work.com"
    try:
        GotifyNotifier(configuration=configuration)
    except ConfigurationError as exec_error:
        pytest.raises(ConfigurationError)
        assert str(exec_error) == "Gotify app token missing in configuration."


@mock.patch("friends_keeper.notifiers.gotify.gotify")
@mock.patch("friends_keeper.notifiers.gotify.GotifyNotifier.build_notification_message")
def test_gotify_notify(build_msg_mock, gotify_mock, two_notifications):
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["gotify"] = dict()
    configuration["notifiers"]["gotify"]["app_token"] = "loco_token_that_does_not_work"
    configuration["notifiers"]["gotify"]["url"] = "https://loco_url_that_does_not_work.com"
    build_msg_mock.return_value = "ANY MSG"
    gotify_mock_object = mock.MagicMock()
    gotify_mock_object.create_message.return_value = True
    gotify_mock.gotify.return_value = gotify_mock_object
    notifier = GotifyNotifier(configuration=configuration)
    notifier.build_notification_message = build_msg_mock
    notifier.notify(two_notifications)


@mock.patch("friends_keeper.notifiers.gotify.gotify")
@mock.patch("friends_keeper.notifiers.gotify.GotifyNotifier.build_notification_message")
def test_gotify_notify_abnormal(build_msg_mock, gotify_mock, two_notifications):
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["gotify"] = dict()
    configuration["notifiers"]["gotify"]["app_token"] = "loco_token_that_does_not_work"
    configuration["notifiers"]["gotify"]["url"] = "https://loco_url_that_does_not_work.com"
    build_msg_mock.return_value = "ANY MSG"
    notifier = GotifyNotifier(configuration=configuration)
    notifier.gotify_obj.create_message = mock.Mock(spec=gotify)
    notifier.gotify_obj.create_message.side_effect = GotifyError(
        mock.MagicMock(status_code=200, headers={"content-type": "application/json"}, text=json.dumps({"status": True}))
    )
    notifier.build_notification_message = build_msg_mock
    try:
        notifier.notify(two_notifications)
    except GotifyError:
        pytest.raises(GotifyError)
