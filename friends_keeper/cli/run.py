"""Run command line module."""
import click

from friends_keeper.core import main_core


@click.group(name="run", invoke_without_command=True, help="Run main core")
@click.pass_context
def run_cli(ctx: click.Context) -> None:
    """Main run command line option group.

    Args:
        ctx (click.Context): Click context passed.
    """
    # click.echo(dir(ctx.obj))
    # if ctx.invoked_subcommand == "friend":
    #     ctx.obj = FriendOptions()
    # elif ctx.invoked_subcommand == "notification":
    #     ctx.obj = NotificationOptions()
    debug_level = ctx.obj.debug_level

    main_core(debug_level=debug_level)
