from unittest import mock

from friends_keeper.constants import DEFAULT_CONFIGURATION
from friends_keeper.notifiers.email import EmailNotifier


def test_email_notifier_initialization():
    notifier = EmailNotifier(configuration=DEFAULT_CONFIGURATION)
    assert notifier.title == "Friends keeper notification"


@mock.patch("friends_keeper.notifiers.email.EmailNotifier.build_notification_message")
def test_email_notify(build_msg_mock, two_notifications):
    notifier = EmailNotifier(configuration=DEFAULT_CONFIGURATION)
    build_msg_mock.return_value = "ANY MSG"
    notifier.build_notification_message = build_msg_mock
    notifier.notify(two_notifications)
    assert build_msg_mock.called == True
