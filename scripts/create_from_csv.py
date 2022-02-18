#!/usr/bin/env python3
import json

import click

from friends_keeper.database import base_database
from friends_keeper.database import engine
from friends_keeper.utils.orm.friends import create_friend


base_database.metadata.create_all(engine)

try:
    import pandas
except ImportError:
    click.echo("ERROR!!! Please install 'pandas'")


__CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=__CONTEXT_SETTINGS, no_args_is_help=True, help="Load friends from CSV file")
@click.option("-f", "--csv-file", type=click.Path(exists=True))
def load_csv(csv_file: str):
    dataframe = pandas.read_csv(csv_file, header=0)
    click.echo(f"Data loaded from csv file:\n{dataframe}")
    click.confirm(text="\nAre you sure, you want to add the data above?", abort=True)

    csv_friends = json.loads(dataframe.to_json(orient="records"))

    for csv_friend in csv_friends:
        create_friend(**csv_friend)


if __name__ == "__main__":
    load_csv()
