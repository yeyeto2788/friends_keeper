"""File notifier module."""
import logging
import os

from datetime import datetime
from typing import List

from friends_keeper.constants import NOTIFICATIONS_FILE_PATH
from friends_keeper.database.notifications import NotificationEvent
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.notifiers.base import BaseNotifier


logger = logging.getLogger(__name__)


class FileNotifier(BaseNotifier):
    """File notifications.

    All notifications go into a given files instead of
    using any other service.

    Args:
        BaseNotifier (friends_keeper.notifiers.base): Base abstract notifier class.
    """

    def __init__(self, configuration: dict):
        """Initialization of the File notifier.

        Args:
            configuration (dict): YAML configuration loaded in JSON format.
        """
        super().__init__(configuration)

    def notify(self, notifications: List[NotificationEvent]) -> None:
        """Notify the user using the file provided on the configuration.

        Args:
            notifications (List[NotificationEvent]): List with notification event
            objects.

        Raises:
            ConfigurationError: Raised when the path on configuration is not valid.
        """
        # TODO: Checking the config should be responsibility of the load_configuration function.
        # Build the notification message
        notification_message = self.build_notification_message(notifications=notifications)

        # TODO: Move check to init and also create the file_path attribute
        config_notifier_file_path = self.configuration["notifiers"]["file"]["path"]

        if config_notifier_file_path:

            config_notifier_file_path = os.path.abspath(config_notifier_file_path)

            if os.path.exists(config_notifier_file_path):
                logger.debug(f"File '{config_notifier_file_path}' exists using it for notification events.")
                create_file = False
            else:
                create_file = True

            notification_file_path = config_notifier_file_path

        else:
            notification_file_path = NOTIFICATIONS_FILE_PATH

        if create_file:

            try:

                with open(config_notifier_file_path, "w"):
                    logger.debug(f"Creating the file '{config_notifier_file_path}' as it does not exists.")
            except OSError:
                logger.error(f"Error occurred trying to create file '{notification_file_path}'.")
                raise ConfigurationError(f"File path '{notification_file_path}' provided in configuration seem wrong.")

        with open(config_notifier_file_path, "a") as file_obj:
            file_obj.write(f"{datetime.now().strftime('%d/%m/%y_%H%M%S')} - {notification_message}")
            logger.info("File notification written.")

    def __repr__(self) -> str:
        """Representation of the file notifier.

        Returns:
            str: String representation of the FileNotifier Object
        """
        # TODO: Add the path used for notifications
        return str({"FileNotifier": {"path": ""}})
