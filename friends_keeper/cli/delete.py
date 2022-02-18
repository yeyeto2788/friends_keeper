"""Delete command line module."""
import sys
import traceback

import click

from friends_keeper.exceptions import ConfigurationError
from friends_keeper.exceptions import FriendsKeeperError
from friends_keeper.extensions import logger
from friends_keeper.utils import load_configuration_file
from friends_keeper.utils.cli import MutuallyExclusiveOption
from friends_keeper.utils.orm.friends import delete_friend
from friends_keeper.utils.orm.friends import get_friend
from friends_keeper.utils.orm.notifications import delete_friend_notification
from friends_keeper.utils.orm.notifications import delete_notification


@click.group(
    name="delete",
    invoke_without_command=True,
    help="Delete friend or notification from database.",
    no_args_is_help=True,
)
@click.pass_context
def delete_cli(ctx: click.Context) -> None:
    """Main delete command line option group.

    Args:
        ctx (click.Context): click context passed.
    """
    pass


@delete_cli.command(name="friend", help="Delete friend and his/her notification events.")
@click.option(
    "--id",
    type=click.INT,
    help="Friend ID.",
    required=True,
)
@click.pass_context
def friends(ctx: click.Context, id: int) -> None:
    """Delete friend based on given friend ID.

    Args:
        ctx (click.Context): click context passed.
        id (int): Friend's ID.
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

        friend = get_friend(friend_id=id)

        if friend:
            click.confirm(f"Are you sure you want to delete '{friend.nickname}' from the database?", abort=True)
            operation_result = delete_friend(friend_id=id)
            if operation_result:
                click.echo(f"Friend {friend.nickname} deleted!")
            else:
                click.echo(f"There was an error trying to delete '{friend.nickname}' from database.")
        else:
            msg = f"Didn't find any friend with id '{id}'\n\nTry getting all friend by executing"
            msg += "\n\t\t'friends_keeper show friends --show-inactive'"
            click.echo(msg)


@delete_cli.command(name="notification", help="Delete friend coming notification event.")
@click.option(
    "--id",
    help="Notification ID.",
    type=click.INT,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["friend_id"],
)
@click.option(
    "--friend-id",
    help="Friend ID.",
    type=click.INT,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["id"],
)
@click.pass_context
def notifications(ctx: click.Context, friend_id: int, id: int) -> None:
    """Delete notification based on given notification event ID or friend's ID.

    Args:
        ctx (click.Context): click context passed.
        friend_id (int): Friend's ID.
        id (int): Notification event ID.
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
            friend = get_friend(friend_id=friend_id)
            click.confirm(f"Are you sure you want to delete notifications for '{friend.nickname}'?", abort=True)

            try:
                delete_friend_notification(friend_id=friend_id)
            except FriendsKeeperError:
                click.echo(f"An error occurred while deleting notifications for friend ID '{friend_id}'")
            else:
                click.echo(f"Notifications for '{friend.nickname}' were deleted")

        else:
            if id is not None:
                try:
                    click.confirm(f"Are you sure you want to delete notification with ID '{id}'?", abort=True)
                    delete_notification(notification_id=id)
                except FriendsKeeperError:
                    click.echo(f"An error occurred while deleting notification with ID '{id}'")
                else:
                    click.echo(f"Notification with ID '{id}' was deleted.")
