"""Main command line interface module.

All different command options groups are added together in this module to centralice the
addition of different command groups.
"""

import click

from friends_keeper.cli.add import add_cli
from friends_keeper.cli.cli_options import CLIOptions
from friends_keeper.cli.delete import delete_cli
from friends_keeper.cli.run import run_cli
from friends_keeper.cli.show import show_cli
from friends_keeper.cli.update import update_cli
from friends_keeper.extensions import logger


__CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=__CONTEXT_SETTINGS, no_args_is_help=True)
@click.option("-v", "--verbose", default=2, count=True)
@click.pass_context
def main_cli(ctx: click.Context, verbose: bool):
    """Main entrypoint for the friends keeper application.

    Args:
        ctx (click.Context): context to be passed onto other command groups.
        verbose (bool): Level of logging.
    """
    click.echo(f"\nUsing debug level {verbose * 10}")
    logger.setLevel(verbose)
    ctx.obj = CLIOptions(debug_level=verbose * 10)


main_cli.add_command(add_cli)
main_cli.add_command(show_cli)
main_cli.add_command(delete_cli)
main_cli.add_command(run_cli)
main_cli.add_command(update_cli)
