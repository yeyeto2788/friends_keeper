"""Friends database utility functions."""
import logging
import random

from typing import List
from typing import Union

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from friends_keeper.database import Session
from friends_keeper.database.friends import Friend
from friends_keeper.database.notifications import NotificationEvent
from friends_keeper.exceptions import DatabaseError
from friends_keeper.utils import generate_next_reminder_date
from friends_keeper.utils.orm import execute_query
from friends_keeper.utils.orm import get_object_from_query
from friends_keeper.utils.orm.notifications import create_notification
from friends_keeper.utils.orm.notifications import delete_friend_notification


logger = logging.getLogger(__name__)


def create_friend(
    nickname: str,
    min_days: int,
    max_days: int,
    name: str = "",
    last_name: str = "",
    relationship: str = "",
) -> Friend:
    """Create friend on the database and the notification event tied to it.

    Args:
        nickname (str): Friend's nickname.
        min_days (int): Minimum days between notifications events.
        max_days (int): Maximum days between notifications events.
        name (str, optional): Friend's name. Defaults to "".
        last_name (str, optional): Friend's last name. Defaults to "".
        relationship (str, optional): Friend relationship. Defaults to "".

    Raises:
        DatabaseError: Raised if error occurred when executing the query.

    Returns:
        Friend: Friend created on the database.
    """
    arguments = {
        "name": name if name else None,
        "last_name": last_name if last_name else None,
        "relationship": relationship if relationship else None,
        "nickname": nickname,
        "min_days": min_days,
        "max_days": max_days,
    }
    friend = Friend(**arguments)
    logger.info(f"Adding a friend to the database with the following information '{str(arguments)}'")

    with Session() as session:
        try:
            session.add(friend)
            session.commit()
            logger.info(f"Friend with ID '{friend.id}' added to the database.")

        except SQLAlchemyError:
            session.rollback()
            msg = "Error occurred trying to add a friend to the database with "
            msg += f"the following information '{str(arguments)}'"
            logger.error(msg)
            raise DatabaseError(msg)

    notification_date = generate_next_reminder_date(random.choice(range(friend.min_days, friend.max_days)))

    logger.info(f"Creating notification event for friend '{friend.id}' with date '{notification_date}'")
    create_notification(friend_id=friend.id, date=notification_date)

    logger.info("Friend and notification event created successfully.")
    return friend


def get_friend(friend_id: int) -> Union[Friend, None]:
    """Get specific friend from database with given friend ID.

    Args:
        friend_id (int): Database friend ID.

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        Union[Friend, None]: Friend found or None.
    """
    query = select(Friend).where(Friend.id == friend_id)
    logger.info(f"Querying database for a friend with ID '{friend_id}'.")

    try:
        friend_found = get_object_from_query(query=query)

    except DatabaseError:
        msg = f"An error occurred trying to get a friend with ID {friend_id}."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        if len(friend_found) > 0:
            logger.info(f"Friend found: {str(friend_found)}")
            return friend_found[0]
        else:
            return None


def get_all_friends(show_inactive: bool = False) -> List[Friend]:
    """Get all friends from database.

    By default we only return the active ones.

    Args:
        show_inactive (bool, optional): Show inactive friends. Defaults to False.

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        List[Friend]: List of friends found on database.
    """
    if show_inactive:
        query = select([Friend]).order_by(Friend.active)

    else:
        filter = Friend.active == True  # noqa: E712
        query = select(Friend).where(filter).order_by(Friend.id)

    logger.info("Querying database for friends")

    try:
        friends = get_object_from_query(query=query)
        logger.info(f"Found friends: '{', '.join([str(friend.id) for friend in friends])}'")

    except DatabaseError:
        msg = f"An error occurred trying to get a friends, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        return friends


def get_next_friend_notification(friend_id: int) -> Union[NotificationEvent, None]:
    """Get comming notification event from a given friend ID.

    Args:
        friend_id (int): Friend's ID

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        Union[NotificationEvent, None]: NotificationEvent found or None
    """
    filter = (NotificationEvent.friend_id == friend_id) & (NotificationEvent.already_notified == False)  # noqa: E712
    query = select(NotificationEvent).where(filter)

    try:
        notifications = get_object_from_query(query=query)
        logger.info(
            f"Found notification events: '{', '.join([str(notification.id) for notification in notifications])}'"
        )

    except DatabaseError:
        msg = f"An error occurred trying to get friend notification events, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        if len(notifications) > 0:
            return notifications[0]

        else:
            return None


def get_all_friend_notifications(friend_id: int) -> List[NotificationEvent]:
    """Get all notification events from a given friend ID.

    Args:
        friend_id (int): Friend's ID.

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        List[NotificationEvent]: All NotificationEvent found.
    """
    filter = NotificationEvent.friend_id == friend_id
    query = select(NotificationEvent).where(filter)
    logger.info(f"Querying database for all notification events for friend '{friend_id}")

    try:
        notifications = get_object_from_query(query=query)
        logger.info(f"Found notification events: '{[notification.id for notification in notifications]}'")

    except DatabaseError:
        msg = f"An error occurred trying to get friend notification events, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        return notifications


def get_friend_notifications_sent(friend_id: int) -> List[NotificationEvent]:
    """Get events triggered from a given friend ID.

    Args:
        friend_id (int): Friend's ID.

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        List[NotificationEvent]: All NotificationEvent sent.
    """
    filter = (NotificationEvent.friend_id == friend_id) & (NotificationEvent.already_notified == True)  # noqa: E712
    query = select(NotificationEvent).where(filter).order_by(NotificationEvent.date)
    logger.info(f"Querying database for sent notification events for friend '{friend_id}")

    try:
        notifications = get_object_from_query(query=query)
        logger.info(f"Found notification events: '{[notification.id for notification in notifications]}'")

    except DatabaseError:
        msg = f"An error occurred trying to get notification events sent, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        return notifications


def delete_friend(friend_id: int) -> bool:
    """Delete friend from database.

    Args:
        friend_id (int): Friend's ID.

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        bool: Whether transaction was successful or not.
    """
    transaction_result = delete_friend_notification(friend_id=friend_id, delete_all=True)
    query = delete(Friend).where(Friend.id == friend_id)

    logger.info(f"Deleting friend with ID '{friend_id}'.")

    if transaction_result:

        try:
            logger.debug(f"Executing query '{str(query)}'")
            operation_result = execute_query(query=query)

        except DatabaseError:
            msg = f"An error occurred trying to delete friend, query: '{str(query)}'."
            logger.error(msg)
            raise DatabaseError(msg)

        else:
            logger.info(f"Notification with ID {friend_id} deleted.")
            return operation_result

    else:
        return False
