"""Gotify notifier module."""
import logging

from typing import List

import gotify

from friends_keeper.database.notifications import NotificationEvent
from friends_keeper.notifiers.base import BaseNotifier


logger = logging.getLogger(__name__)


class GotifyNotifier(BaseNotifier):
    """Gotify notifications.

    All notifications are done using Gotify API so push messages are delivered
    to users on Gotify clients.

    Args:
        BaseNotifier (friends_keeper.notifiers.base): Base abstract notifier class.
    """

    def __init__(self, configuration: dict):
        """Initialization of the Gotify notifier.

        Args:
            configuration (dict): YAML configuration loaded in JSON format.
        """
        logger.info("Instantiating the gotify module")
        # TODO: Get this values from configuration.
        self.base_url = "https://notifications.local.juanbiondi.com"
        self._token = "A2URDOuPTEqwrAc"

        try:
            self.gotify_obj = gotify.gotify(
                base_url=self.base_url,
                app_token=self._token,
            )

        except gotify.GotifyError:
            raise

        super().__init__(configuration)

    def notify(self, notifications: List[NotificationEvent]) -> None:
        """Notify the user using the gotify api.

        Args:
            notifications (List[NotificationEvent]): List with notification event
            objects.
        """
        logger.debug("Building message")

        notification_message = self.build_notification_message(notifications=notifications)

        try:
            logger.debug("Sending gotify message")
            self.gotify_obj.create_message(
                message=notification_message,
                title=self.title,
                priority=0,
            )

        except gotify.GotifyError:
            logger.error("Error occurred trying to send the gotify message.")
            raise

        else:
            logger.info("Gotify message sent")

    def __repr__(self) -> str:
        """String representation of GotifyNotifier.

        Returns:
            str: String representation of the object.
        """
        return str(
            {
                "GotifyNotifier": {
                    "url": self.base_url,
                },
            }
        )
