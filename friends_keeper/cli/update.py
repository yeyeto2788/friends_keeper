"""Update command line module."""
import sys
import traceback

from datetime import datetime

import click

from friends_keeper.constants import DATE_FORMAT
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.extensions import logger
from friends_keeper.utils import load_configuration_file
from friends_keeper.utils.cli import MutuallyExclusiveOption
from friends_keeper.utils.orm.friends import get_friend
from friends_keeper.utils.orm.friends import get_next_friend_notification
from friends_keeper.utils.orm.notifications import create_notification
from friends_keeper.utils.orm.notifications import get_notification
from friends_keeper.utils.orm.notifications import update_notification_event_date


@click.group(
    name="update",
    invoke_without_command=True,
    help="Update friend or notification on the database",
    no_args_is_help=True,
)
@click.pass_context
def update_cli(ctx: click.Context) -> None:
    """Main update command line option group.

    Mainly used to update friend information or notification event dates.

    Args:
        ctx (click.Context): click context passed.
    """
    pass


@update_cli.command(name="friend", help="Update a friend.")
@click.option(
    "-n",
    "--nickname",
    type=click.STRING,
    required=True,
    help="Nickname for the friend",
)
@click.option(
    "--name",
    type=click.STRING,
    default="",
    help="Friend's name.",
    show_default=True,
)
@click.option(
    "--last-name",
    type=click.STRING,
    default="",
    help="Friend's last name.",
    show_default=True,
)
@click.option(
    "--relationship",
    type=click.STRING,
    default="",
    help="Person relationship.",
    show_default=True,
)
@click.option(
    "--min-days",
    type=click.IntRange(min=1, max=15),
    default=7,
    help="Minimum days between reminders.",
    show_default=True,
)
@click.option(
    "--max-days",
    type=click.IntRange(min=16, max=30),
    default=20,
    help="Maximum days between reminders",
    show_default=True,
)
@click.pass_context
def friend(
    ctx: click.Context, nickname: str, min_days: int, max_days: int, name: str, last_name: str, relationship: str
) -> None:
    """Update friend information.

    Args:
        ctx (click.Context): click context passed.
        nickname (str): Friend's nickname.
        min_days (int): Minimum days between notifications events.
        max_days (int): Maximum days between notifications events.
        name (str): Friend's name.
        last_name (str): Friend's last name.
        relationship (str): Friend relationship.

    Raises:
        NotImplementedError: Not possible to edit friend information at the moment.
    """
    # Get configuration
    try:
        # Load config to check for any changes
        _ = load_configuration_file()

    except ConfigurationError:
        exec_info = sys.exc_info()
        logger.error("Error occurred loading configuration file.")
        traceback.print_exception(*exec_info)
        raise

    else:
        # TODO: What it is allowed to be edit?
        raise NotImplementedError


@update_cli.command(name="notification", help="Update a notification event date for a given friend ID.")
@click.option(
    "--friend-id",
    type=click.INT,
    help="Friend ID to which add a notification.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["notification_id"],
)
@click.option(
    "--notification-id",
    type=click.INT,
    help="Notification event ID to which add a notification.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["friend_id"],
)
@click.option(
    "--date",
    "new_date",
    type=click.DateTime(formats=[DATE_FORMAT]),
    help="New date for the notification event.",
)
@click.pass_context
def notification(ctx: click.Context, friend_id: int, new_date: datetime.date, notification_id: int) -> None:
    """Update notification event date.

    Args:
        ctx (click.Context): click context passed.
        friend_id (int): Friend's ID.
        new_date (datetime.date): New date to be assigned to the notification event.
        notification_id (int): Notification event ID.
    """
    # Get configuration
    try:
        # Load config to check for any changes
        _ = load_configuration_file()

    except ConfigurationError:
        exec_info = sys.exc_info()
        logger.error("Error occurred loading configuration file.")
        traceback.print_exception(*exec_info)
        raise

    else:

        if friend_id is not None:
            friend = get_friend(friend_id)

            if friend:
                notification = get_next_friend_notification(friend.id)

                if not notification:
                    confirm_message = f"\nThere are not notification events for the user '{friend.id}' "
                    confirm_message += "to be trigger, do want to create it?"
                    click.confirm(confirm_message, abort=True)

                    new_notification = create_notification(friend_id=friend_id, date=new_date)
                    success_message = f"\nNotification event with ID '{new_notification.id}' "
                    success_message += f"created with date '{new_notification.date.strftime(DATE_FORMAT)}'"
                    click.echo(success_message)

                else:
                    operation_result = update_notification_event_date(friend_id=friend.id, new_date=new_date)

                    if operation_result:
                        operation_message = f"\nNotification for friend '{friend.nickname}' "
                        operation_message += f"updated with date '{new_date.strftime(DATE_FORMAT)}'"
                        click.echo(operation_message)

            else:
                click.echo(f"\nSeems like there is no friend with the id '{friend_id}'")
                sys.exit(-1)
        else:
            notification = get_notification(notification_id=notification_id)
            friend = get_friend(friend_id=notification.friend_id)

            operation_result = update_notification_event_date(friend_id=friend.id, new_date=new_date)

            if operation_result:
                operation_message = f"\nNotification for friend '{friend.nickname}' "
                operation_message += f"updated with date '{new_date.strftime(DATE_FORMAT)}'"
                click.echo(operation_message)
