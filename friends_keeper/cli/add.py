"""Add command line module."""
import random
import sys
import traceback

import click

from friends_keeper.constants import DATE_FORMAT
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.extensions import logger
from friends_keeper.utils import generate_next_reminder_date
from friends_keeper.utils import load_configuration_file
from friends_keeper.utils.orm.friends import create_friend
from friends_keeper.utils.orm.friends import get_friend
from friends_keeper.utils.orm.friends import get_next_friend_notification
from friends_keeper.utils.orm.notifications import create_notification


@click.group(
    name="add", invoke_without_command=True, help="Add friend or notification to the database", no_args_is_help=True
)
@click.pass_context
def add_cli(ctx: click.Context) -> None:
    """Main addition command line option group.

    Mainly used to add Friend or Notification events.

    Args:
        ctx (click.Context): click context passed.
    """
    # click.echo(dir(ctx.obj))
    # if ctx.invoked_subcommand == "friend":
    #     ctx.obj = FriendOptions()
    # elif ctx.invoked_subcommand == "notification":
    #     ctx.obj = NotificationOptions()
    pass


@add_cli.command(name="friend", help="Add a friend to be reminded.")
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
    help="Minimum days between reminders",
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
    """Add new friend to the database.

    Args:
        ctx (click.Context): click context passed.
        nickname (str): Friend's nickname.
        min_days (int): Minimum days between notifications events.
        max_days (int): Maximum days between notifications events.
        name (str): Friend's name.
        last_name (str): Friend's last name.
        relationship (str): Friend relationship.
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

        friend = create_friend(
            nickname=nickname,
            min_days=min_days,
            max_days=max_days,
            name=name,
            last_name=last_name,
            relationship=relationship,
        )
        click.echo(f"Friend '{friend.nickname}' added.")
        # TODO: Get next notification and print it on the screen


@add_cli.command(name="notification", help="Add a notification event for a given friend ID.")
@click.option(
    "--friend-id",
    type=click.INT,
    help="Friend ID to which add a notification",
)
@click.pass_context
def notification(ctx: click.Context, friend_id: int) -> None:
    """Add a notification event to a given friend.

    Args:
        ctx (click.Context): click context passed.
        friend_id (int): Friend's ID.
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

        friend = get_friend(friend_id)

        if friend:
            notification = get_next_friend_notification(friend.id)

            if notification is not None:
                msg = f"There is already notification event for the user '{friend.id}' "
                msg += f"to be trigger at '{notification.date.strftime(DATE_FORMAT)}'"
                click.echo(msg)
                sys.exit(0)

            else:
                random_day = random.choice(range(friend.min_days, friend.max_days))
                notification_date = generate_next_reminder_date(days=random_day)
                notification = create_notification(friend_id=friend_id, date=notification_date)
                msg = f"Notification event with ID '{notification.id}' "
                msg += f"created with date '{notification.date.strftime(DATE_FORMAT)}'"
                click.echo(msg)

        else:
            click.echo(f"Seems like there is no friend with the id '{friend_id}'")
            sys.exit(-1)
