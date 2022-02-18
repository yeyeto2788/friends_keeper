"""Show command line module."""
import json
import sys
import traceback

from typing import Union

import click

from prettytable import PrettyTable

from friends_keeper.constants import DATE_FORMAT
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.extensions import logger
from friends_keeper.utils import load_configuration_file
from friends_keeper.utils.orm.friends import get_all_friend_notifications
from friends_keeper.utils.orm.friends import get_all_friends
from friends_keeper.utils.orm.friends import get_friend
from friends_keeper.utils.orm.notifications import get_coming_notifications


@click.group(name="show", invoke_without_command=True, help="Show information about stored data", no_args_is_help=True)
def show_cli() -> None:
    """Main show command line option group."""
    pass


@show_cli.command(name="friends", help="Show friends information")
@click.option("--show-inactive", type=click.BOOL, default=False, show_default=True, help="Show inactive users.")
def friends(show_inactive: bool) -> None:
    """Show all friends on database.

    Args:
        show_inactive (bool): Whether show or not inactive friends.
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

        friends = get_all_friends(show_inactive=show_inactive)

        if len(friends) > 0:
            click.echo("\nFriends in database")
            table_printer = PrettyTable()
            table_printer.field_names = ["Friend ID", "Nickname", "Min. days", "Max. days", "Active"]

            for friend in friends:
                table_printer.add_row([friend.id, friend.nickname, friend.min_days, friend.max_days, friend.active])

            click.echo(table_printer.get_string())
        else:
            click.echo("No friends found.")


@show_cli.command(name="notifications", help="Show coming notifications")
@click.option(
    "-f", "--friend-id", type=click.INT, default=None, help="Retrieve friend specific notifications.", show_default=True
)
def notifications(friend_id: Union[str, None]) -> None:
    """Show all notification events comming for a given friend.

    Args:
        friend_id (Union[str, None]): Friend's ID.
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
            notifications = get_all_friend_notifications(friend_id=friend_id)
        else:
            notifications = get_coming_notifications()

        if len(notifications) > 0:
            click.echo("\nComing notifications events:")

            table_printer = PrettyTable()
            table_printer.field_names = ["Notification ID", "Nickname", "Date"]

            for notification in notifications:
                friend = get_friend(friend_id=notification.friend_id)
                table_printer.add_row([notification.id, friend.nickname, notification.date.strftime(DATE_FORMAT)])

            click.echo(table_printer.get_string())

        else:
            click.echo("No notifications found.")


@show_cli.command(name="configuration", help="Show friends_keeper configuration")
def configuration() -> None:
    """Show current configuration used."""
    # Get configuration
    try:
        # Load config to check for any changes
        configuration = load_configuration_file()

    except ConfigurationError:
        exec_info = sys.exc_info()
        logger.error("Error occurred loading configuration file.")
        traceback.print_exception(*exec_info)
        raise

    else:
        click.echo(f"Used configuration:\n {str(json.dumps(configuration, indent=2))}")
