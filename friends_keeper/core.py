"""Main core logic.

The idea behind this logic is that it should get called
once a day so it gathers the notifications, the friends to
action on and notify the user about those friends to contact.

After notification, the event should be marked as `already_notified=True`
 and generate the next notification event on the database.
"""
import logging
import random
import sys
import traceback

from typing import Union

from friends_keeper.exceptions import ConfigurationError
from friends_keeper.notifiers import NotifierFactory
from friends_keeper.utils import generate_next_reminder_date
from friends_keeper.utils import load_configuration_file
from friends_keeper.utils.orm.friends import get_friend
from friends_keeper.utils.orm.notifications import create_notification
from friends_keeper.utils.orm.notifications import get_today_notifications
from friends_keeper.utils.orm.notifications import mark_notification_as_done


logger = logging.getLogger(__name__)


def main_core(debug_level: Union[int, None] = None):
    """Main core logic definition.

    Steps:
      - Get notifications.
      - Get notifications' friends
      - Build mesage.
      - Notify user.
      - Mark notification event as `already_done=True`.
      - Create new notification event.

    Args:
        debug_level (Union[int, None], optional): Error level to be used while executing. Defaults to None.
    """
    # without setting the level everywhere
    if debug_level is not None:
        logger.setLevel(debug_level)

    # Get configuration
    try:
        configuration = load_configuration_file()

    except ConfigurationError:
        exec_info = sys.exc_info()
        logger.error("Error occurred loading configuration file.")
        traceback.print_exception(*exec_info)
        raise

    else:

        # Get today notifications
        notifications = get_today_notifications()
        logger.debug(f"Found notifications: {notifications}")

        # If there are notifications, do notify
        if notifications:

            # Get notifier and notify
            try:
                notifiers = NotifierFactory.get_notifiers(configuration=configuration)

            except (NotImplementedError, ConfigurationError):
                exec_info = sys.exc_info()
                logger.error("Error occurred trying to send the notification")
                traceback.print_exception(*exec_info)

            else:

                for notifier in notifiers:
                    notifier.notify(notifications)

                for notification in notifications:
                    # Mark notifications as done
                    logger.debug(f"Marking notification '{notification.id}' as done.")
                    friend = get_friend(friend_id=notification.friend_id)
                    mark_notification_as_done(notification.id)
                    # Create new notification event
                    random_day = random.choice(range(friend.min_days, friend.max_days))
                    notification_date = generate_next_reminder_date(days=random_day)
                    new_notification = create_notification(friend_id=friend.id, date=notification_date)
                    logger.debug(
                        f"New notification event '{new_notification.id}' created at '{new_notification.date}'."
                    )

        else:
            logger.info("We didn't find any notifications for today")
