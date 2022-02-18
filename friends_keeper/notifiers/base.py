"""Base notifier module."""
import logging
import random

from abc import ABC
from abc import abstractmethod
from typing import List

from friends_keeper.constants import ACTIONS
from friends_keeper.constants import REMINDING_NOTES
from friends_keeper.database.notifications import NotificationEvent
from friends_keeper.utils.orm.friends import get_friend


logger = logging.getLogger(__name__)


class BaseNotifier(ABC):
    """Base notifier to be inherited by other implementations.

    Args:
        ABC (abc.ABC): Abstract class.
    """

    def __init__(self, configuration: dict):
        """Initialization of the object.

        Args:
            configuration (dict): YAML configuration loaded in JSON format.
        """
        if configuration["notifications"]["title"]:
            self.title = configuration["notifications"]["title"]
        else:
            self.title = "Friends keeper notification"

        self.configuration = configuration

    @abstractmethod
    def notify(self, message: str) -> None:
        """Abstract method definition so all object get the same method.

        Args:
            message (str): Message to be sent.
        """
        pass

    def build_notification_message(self, notifications: List[NotificationEvent]) -> str:
        """Build notification message using information from notification event passed.

        Args:
            notifications (List[NotificationEvent]): List with notification event
            objects.

        Returns:
            str: Message to be sent.
        """
        # Join all friend together
        friends = ", ".join([get_friend(notification.friend_id).nickname for notification in notifications])
        action = random.choice(ACTIONS).upper()

        logger.debug(f"Found friends: {friends}")

        if self.configuration["notifications"]["message"]:
            notification_message = self.configuration["notifications"]["message"].format(
                action=action, friend_name=friends
            )
            logger.debug(f"Using default message '{notification_message}'")

        else:
            # Build notification message
            notification_message = random.choice(REMINDING_NOTES).format(action=action, friend_name=friends)
            logger.debug(f"Built message: '{notification_message}'")

        return notification_message
