"""Options objects to be used within click context."""
import json


class CLIOptions:
    """Main CLI options."""

    def __init__(self, debug_level: int):
        """Initialization of the CLI options.

        Args:
            debug_level (int): Level for logging
            (DEBUG=1, INFO=2, WARNING=3, ERROR=4, CRITICAL=5)
        """
        self.debug_level = debug_level

    def __repr__(self) -> str:
        """JSON string representation of the CLI options."""
        attributes = {key: value for key, value in self.__dict__.items()}
        return json.dumps(attributes)
