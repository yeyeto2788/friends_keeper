#!/usr/bin/env python3
import sys
import traceback
import click

from friends_keeper.cli import main_cli
from friends_keeper.database import base_database, engine

base_database.metadata.create_all(engine)


if __name__ == "__main__":

    try:
        main_cli()

    except KeyError:
        exec_info = sys.exc_info()
        click.echo("An error occurred executing the script\n\n")
        traceback.print_exception(*exec_info)
        sys.exit(-1)
