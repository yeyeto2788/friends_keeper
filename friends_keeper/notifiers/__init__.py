"""Notifiers modules with notifier factory."""
from abc import ABC
from typing import List

from friends_keeper.constants import NOTIFIER_TYPES
from friends_keeper.extensions import logger
from friends_keeper.notifiers.base import BaseNotifier
from friends_keeper.notifiers.email import EmailNotifier
from friends_keeper.notifiers.file import FileNotifier
from friends_keeper.notifiers.gotify import GotifyNotifier


class NotifierFactory(ABC):
    """Notifier factory to get the different notifiers.

    Args:
        ABC (abc.ABC): Abstract class
    """

    def get_notifiers(configuration: dict) -> List[BaseNotifier]:
        """Get notifier from the configuration passed.

        Args:
            configuration (dict): YAML configuration loaded as dict.

        Raises:
            NotImplementedError: Raised when notifier is not implemented.

        Returns:
            List[BaseNotifier]: List with loaded notifiers.
        """
        notifiers = list()
        notifier_types = configuration["notifications"]["type"]

        for notifier_type in notifier_types:

            if notifier_type not in NOTIFIER_TYPES:
                logger.error(f"There is no such '{notifier_type}' notifier type.")
                raise NotImplementedError(f"We do have such notifier '{notifier_type}'")

            else:

                if notifier_type == NOTIFIER_TYPES.file:
                    logger.debug(f"Adding '{NOTIFIER_TYPES.file}' notifier.")
                    notifiers.append(FileNotifier(configuration=configuration))

                elif notifier_type == NOTIFIER_TYPES.gotify:
                    logger.debug(f"Adding '{NOTIFIER_TYPES.gotify}' notifier.")
                    notifiers.append(GotifyNotifier(configuration=configuration))

                elif notifier_type == NOTIFIER_TYPES.email:
                    logger.debug(f"Adding '{NOTIFIER_TYPES.email}' notifier.")
                    notifiers.append(EmailNotifier(configuration=configuration))

        else:
            logger.debug(f"Using these notifiers: '{notifiers}'.")
            return notifiers
