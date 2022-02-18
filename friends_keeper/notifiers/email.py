"""Email notifier module."""
import logging

from datetime import datetime
from typing import List

from friends_keeper.database.notifications import NotificationEvent
from friends_keeper.notifiers.base import BaseNotifier


logger = logging.getLogger(__name__)


class EmailNotifier(BaseNotifier):
    """Email notifications.

    All notifications are sent via mail.

    Args:
        BaseNotifier (friends_keeper.notifiers.base): Base abstract notifier class.
    """

    def __init__(self, configuration: dict):
        """Initialization of the email notifier.

        Args:
            configuration (dict): YAML configuration loaded in JSON format.
        """
        super().__init__(configuration)

    def notify(self, notifications: List[NotificationEvent]) -> None:
        """Notify user via email.

        Args:
            notifications (List[NotificationEvent]): List with notification event
            objects.
        """
        # TODO: Implement real logic
        notification_message = self.build_notification_message(notifications=notifications)
        print(f"{datetime.now().strftime('%d/%m/%y_%H%M%S')} - {notification_message}")

    def __repr__(self) -> str:
        """String representation of EmailNotifier.

        Returns:
            str: String representation of the object.
        """
        return "EmailNotifier"
