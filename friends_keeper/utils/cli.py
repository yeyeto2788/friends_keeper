"""Command line utility functions."""
from typing import Any
from typing import List
from typing import Mapping
from typing import Tuple

import click

from click import Option
from click import UsageError


class MutuallyExclusiveOption(Option):
    """Option for CLI command that excludes other options.

    This is done so within the same command you can have 2 options
     that could exclude the usage of the other option if the first
     one is present.

    Args:
        Option (click.Option): Options base object
    """

    def __init__(self, *args, **kwargs):
        """Initialization of the mutually exclusive option."""
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help = kwargs.get("help", "")

        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help + (" NOTE: This argument is mutually exclusive with " " arguments: [" + ex_str + "].")

        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(
        self, ctx: click.Context, opts: Mapping[str, Any], args: List[str]
    ) -> Tuple[Any, List[str]]:
        """Parse the options passed to the object and its values.

        Args:
            ctx (click.Context): Click context.
            opts (Mapping[str, Any]): Option with values.
            args (List[str]): [description]

        Raises:
            UsageError: Raised when both options are passed to the commands.

        Returns:
            Tuple[Any, List[str]]: Value, Arguments after parsing the values
             passed to the option.
        """
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)
