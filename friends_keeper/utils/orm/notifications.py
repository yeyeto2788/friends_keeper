"""Common notifications event utility functions."""
import logging

from datetime import datetime
from typing import List

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from friends_keeper.database import Session
from friends_keeper.database.notifications import NotificationEvent
from friends_keeper.exceptions import DatabaseError
from friends_keeper.utils.orm import execute_query
from friends_keeper.utils.orm import get_object_from_query


logger = logging.getLogger(__name__)


def get_today_notifications() -> List[NotificationEvent]:
    """Get notification event of current day for all friends.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        List[NotificationEvent]: List with obtained notification event objects.
    """
    filter = (NotificationEvent.already_notified == False) & (  # noqa: E712
        NotificationEvent.date == datetime.today().date()
    )
    query = select(NotificationEvent).where(filter)
    logger.debug("Querying database for today's notification events")

    try:
        notifications = get_object_from_query(query=query)
        logger.debug(f"Found notification events'{[notification.id for notification in notifications]}'")

    except DatabaseError:
        msg = f"An error occurred trying to get todays notification events, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        return notifications


def create_notification(friend_id: int, date: datetime.date) -> NotificationEvent:
    """Create friend notification event.

    Args:
        friend_id (int): ID to which the notification is assigned.
        date (datetime.date): Date of the notification event.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        NotificationEvent: Notification even object created.
    """
    notification = NotificationEvent(friend_id=friend_id, date=date)
    logger.info(f"Notification: {str(notification)} will be created.")

    with Session() as session:
        try:
            session.add(notification)
            session.commit()
            logger.info(f"Notification ID '{notification.id}' created")

        except SQLAlchemyError:
            session.rollback()
            msg = "An error occurred trying to create the notification."
            logger.error(msg)
            raise DatabaseError(msg)

        else:
            return notification


def update_notification_event_date(friend_id: int, new_date: datetime.date) -> bool:
    """Update notification event date.

    New date gets assigned to the notification event of a given friend.

    Args:
        friend_id (int): ID of the friend the notification event belongs to.
        new_date (datetime.date): New date to be assigned.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        bool: Whether operation was successful or not.
    """
    query = update(NotificationEvent).where(NotificationEvent.friend_id == friend_id).values(date=new_date)
    logger.info(f"Updating notification event from friend ID '{friend_id}' with '{new_date}' date.")

    try:
        operation_result = execute_query(query=query)

    except DatabaseError:
        msg = f"An error occurred trying to update notification events, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        logger.info(f"Notification updated with new date {new_date}.")
        return operation_result


def delete_notification(notification_id: int) -> bool:
    """Delete notification event by ID.

    Args:
        notification_id (int): ID of the notification event to be deleted.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        bool: Whether operation was successful or not.
    """
    query = delete(NotificationEvent).where(NotificationEvent.id == notification_id)
    logger.info(f"Deleting notification ID '{notification_id}'.")

    try:
        operation_result = execute_query(query=query)

    except DatabaseError:
        msg = f"An error occurred trying to delete notification event, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        logger.info(f"Notification with ID {notification_id} deleted.")
        return operation_result


def delete_friend_notification(friend_id: int, delete_all: bool = False) -> bool:
    """Delete notification events from a given friend.

    Args:
        friend_id (int): ID of the friend to look the notification event.
        delete_all (bool, optional): Whether delete or not all
        notifications from given friend. Defaults to False.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        bool: Whether operation was successful or not.
    """
    if delete_all:
        # Delete them all.
        query = delete(NotificationEvent).where(NotificationEvent.friend_id == friend_id)

    else:
        # Delete the ones that haven't been triggered/notified
        filter = (NotificationEvent.friend_id == friend_id) & (
            NotificationEvent.already_notified == False  # noqa: E712
        )
        query = delete(NotificationEvent).where(filter)

    logger.info(f"Deleting notification{'s' if delete_all else ''} from friend '{friend_id}'.")

    try:
        operation_result = execute_query(query=query)

    except DatabaseError:
        msg = f"Error occurred deleting notification{'s' if delete_all else ''}."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        logger.info(f"Notification{'s' if delete_all else ''} from friend '{friend_id}' deleted.")
        return operation_result


def mark_notification_as_done(notification_id: int) -> bool:
    """Set the `already_notified` attribute to `True`.

    Args:
        notification_id (int): ID of the notification event.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        bool: Whether operation was successful or not.
    """
    query = update(NotificationEvent).where(NotificationEvent.id == notification_id).values(already_notified=True)
    logger.info(f"Marking notification ID '{notification_id}' as done.")

    try:
        operation_result = execute_query(query=query)

    except DatabaseError:
        msg = f"An error occurred trying to mark notification event as done, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        logger.info(f"Notification with ID {notification_id} updated.")
        return operation_result


def get_coming_notifications() -> List[NotificationEvent]:
    """Get the next notification from tomorrow on.

    Raises:
        DatabaseError: Raised if error occurred while executing transaction.

    Returns:
        List[NotificationEvent]: List with notification event objects
    """
    query = (
        select(NotificationEvent)
        .where(NotificationEvent.date >= datetime.today().date())
        .order_by(NotificationEvent.date)
    )
    logger.info("Querying database for comming notification events")

    try:
        notifications = get_object_from_query(query=query)
        logger.info(f"Found notification events: '{[notification.id for notification in notifications]}'")

    except DatabaseError:
        msg = f"An error occurred trying to get notification events, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        return notifications


def get_notification(notification_id: int) -> NotificationEvent:
    """Get notification event object from given ID.

    Args:
        notification_id (int): Notification event ID.

    Raises:
        DatabaseError: Raised when executing query.

    Returns:
        NotificationEvent: NotificationEvent found.
    """
    query = select(NotificationEvent).where(NotificationEvent.id == notification_id)
    logger.info(f"Querying database for notification event '{notification_id}'")

    try:
        notification = get_object_from_query(query=query)
        logger.info(f"Found notification event: '{notification}'")

    except DatabaseError:
        msg = f"An error occurred trying to get notification events, query: '{str(query)}'."
        logger.error(msg)
        raise DatabaseError(msg)

    else:
        return notification
