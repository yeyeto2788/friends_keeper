import os

from unittest import mock

import pytest

from friends_keeper.constants import DEFAULT_CONFIGURATION
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.notifiers.file import FileNotifier


def test_file_notifier_initialization():
    notifier = FileNotifier(configuration=DEFAULT_CONFIGURATION)
    assert notifier.title == "Friends keeper notification"


@pytest.mark.parametrize(
    "file_path, read_file, expected, delete_file",
    [
        ("./test_notification.txt", "./test_notification.txt", " - ANY MSG", True),
        ("./test_notification.txt", "./test_notification.txt", " - ANY MSG", False),
        ("./test_notification.txt", "./test_notification.txt", " - ANY MSG", True),
        ("./test_notification111.txt", "./test_notification111.txt", " - ANY MSG", True),
    ],
)
@mock.patch("friends_keeper.notifiers.file.FileNotifier.build_notification_message")
def test_file_notify(build_msg_mock, two_notifications, file_path, read_file, expected, delete_file):
    test_file_path = os.path.abspath(file_path)
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["file"]["path"] = test_file_path
    notifier = FileNotifier(configuration=configuration)
    msg = "ANY MSG"
    build_msg_mock.return_value = msg
    notifier.build_notification_message = build_msg_mock
    notifier.notify(two_notifications)

    with open(read_file) as file_obj:
        file_content = file_obj.read()

    assert expected in file_content

    if delete_file:
        os.remove(read_file)


@mock.patch("friends_keeper.notifiers.file.FileNotifier.build_notification_message")
def test_file_notify_no_file_path(build_msg_mock, two_notifications):
    test_file_path = os.path.abspath("./notifications.txt")
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["file"]["path"] = ""
    notifier = FileNotifier(configuration=configuration)
    msg = "ANY MSG"
    build_msg_mock.return_value = msg
    notifier.build_notification_message = build_msg_mock
    notifier.notify(two_notifications)

    with open(test_file_path) as file_obj:
        file_content = file_obj.read()

    assert f" - {msg}" in file_content


@mock.patch("friends_keeper.notifiers.file.open")
@mock.patch("friends_keeper.notifiers.file.FileNotifier.build_notification_message")
def test_file_notify_abnormal(build_msg_mock, open_mock, two_notifications):
    test_file_path = os.path.abspath("./notifications_TO_DELETE.txt")
    configuration = DEFAULT_CONFIGURATION
    configuration["notifiers"]["file"]["path"] = test_file_path
    notifier = FileNotifier(configuration=configuration)
    msg = "ANY MSG"
    open_mock.side_effect = OSError
    build_msg_mock.return_value = msg
    notifier.build_notification_message = build_msg_mock

    try:
        notifier.notify(two_notifications)
    except ConfigurationError:
        pytest.raises(ConfigurationError)
