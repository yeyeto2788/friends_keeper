"""Application utilities module."""
import logging
import os
import sys

from datetime import datetime
from datetime import timedelta

import jsonschema
import yaml

from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError

from friends_keeper.constants import CONFIGURATION_FILE_PATH
from friends_keeper.constants import NOTIFIER_TYPES
from friends_keeper.constants import YAML_SCHEMA
from friends_keeper.exceptions import ConfigurationError
from friends_keeper.exceptions import FriendsKeeperError


logger = logging.getLogger(__name__)


def load_configuration_file() -> dict:
    """Load application configuration file.

    Returns:
        dict: Configuration read from the file on the environment variable `CONFIGURATION_FILE_PATH`
    """
    config_file_path = os.path.abspath(CONFIGURATION_FILE_PATH)

    with open(config_file_path) as config_file:
        try:
            logger.info(f"Loading configuration from '{config_file_path}'")
            configuration = yaml.safe_load(config_file)

        except yaml.YAMLError as exec_error:

            if hasattr(exec_error, "problem_mark"):
                mark = exec_error.problem_mark
                msg = f"Error in configuration file: ({mark.line+1}:{mark.column+1})"
                logger.error(msg)
            raise ConfigurationError(exec_error.message)

        else:
            is_config_ok = check_config(configuration=configuration)

            if is_config_ok:
                return configuration
            else:
                raise ConfigurationError("Error occurred while verifying the configuration.")


def is_valid_config_schema(configuration: dict) -> bool:
    """Check whether the configuration file schema is right or not.

    Args:
        configuration (dict): YAML configuration loaded into dict format.

    Raises:
        ConfigurationError: Raise when there is an issue on the configuration file.

    Returns:
        bool: Whether the configuration schema is valid or not.
    """
    result = False

    try:
        logger.debug("Validating configuration file content.")
        jsonschema.validate(instance=configuration, schema=YAML_SCHEMA)
        result = True

    except ValidationError as exec_error:
        msg = f"Error in configuration file '{exec_error.message}'"
        logger.error(msg)
        raise ConfigurationError(msg)

    except SchemaError:
        error_msg = f"Unexpected error occurred validating the configuration '{str(configuration)}' "
        error_msg += f"against schema '{str(YAML_SCHEMA)}'"
        logger.error(error_msg)
        sys.exit(-1)
    else:
        logger.debug("Config file schema is valid.")
        return result


def check_config(configuration: dict) -> bool:
    """Check file configuration to use on the application.

    Args:
        configuration (dict): YAML configuration loaded into dict format.

    Raises:
        ConfigurationError: Raised when something happened validating any part of
         the configuration file.

    Returns:
        bool: Whether the configuration passed is valid or not.
    """
    is_config_ok = False

    try:
        is_valid_config_schema(configuration=configuration)
    except FriendsKeeperError:
        raise

    else:

        try:
            logging_config = configuration["logging"]
            is_logging_ok = validate_logging_configuration(configuration=logging_config)

            notifications_config = configuration["notifications"]
            is_notifications_ok = validate_notifications_config(configuration=notifications_config)

            notifiers_config = configuration["notifiers"]
            are_notifiers_ok = validate_notificatiers_configuration(configuration=notifiers_config)

        except FriendsKeeperError:
            raise ConfigurationError("Error occurred validating the configuration")

        else:
            is_config_ok = is_logging_ok and is_notifications_ok and are_notifiers_ok
            return is_config_ok


def validate_logging_configuration(configuration: dict) -> bool:
    """Check if logging configuration is valid or not.

    Args:
        configuration (dict): YAML configuration loaded into dict format.

    Raises:
        FileNotFoundError: Raised if logging path does not
        exists and cannot be created.

    Returns:
        bool: Whether the configuration passed is valid or not.
    """
    is_config_ok = False

    logging_configuration = dict()

    # Get logging level and apply that
    log_level = configuration["debug_level"]
    logger.setLevel(log_level)

    # Check logging path
    log_file_path = configuration["path"]

    if os.path.exists(log_file_path):
        logger.info(f"Using '{log_file_path}' for logging")
        logging_configuration["path"] = log_file_path
        is_config_ok = True
    else:
        try:
            logger.info(f"Creating log file at '{log_file_path}'")
            with open(log_file_path, "w"):
                logger.info(f"Log file '{log_file_path}' created.")
        except OSError:
            logger.error(f"Error occurred creating file '{log_file_path}'")
            raise FileNotFoundError(f"Could not create the file '{log_file_path}'")
        else:
            is_config_ok = True

    return is_config_ok


def validate_notifications_config(configuration: dict) -> bool:
    """Check if notifications configuration is valid or not.

    Args:
        configuration (dict): YAML configuration loaded into dict format.

    Raises:
        ConfigurationError: Raised if notification type is not valid.

    Returns:
        bool: Whether the configuration passed is valid or not.
    """
    is_config_ok = False

    # Check notification type
    notification_types = configuration["type"]

    for notif_type in notification_types:
        if notif_type not in NOTIFIER_TYPES:
            raise ConfigurationError(f"The notification type '{notif_type}' is not implemented")

    # TODO: check message and title against know variables/attributes from friends table.

    is_config_ok = True

    return is_config_ok


def validate_notificatiers_configuration(configuration: dict) -> bool:
    """Check whether the configuration for notifiers is valid.

    Args:
        configuration (dict): YAML configuration loaded into dict format.

    Raises:
        ConfigurationError: Raised if notification type is not valid.

    Returns:
        bool: Whether the configuration passed is valid or not.
    """
    # TODO: Check if there is something to be done for real
    is_config_ok = True
    return is_config_ok


def generate_next_reminder_date(days: int) -> datetime.date:
    """Get next date to add into the notifications event.

    Args:
        days (int): Integer with the amount of days to sum on current date.

    Returns:
        datetime.date: Next date generated.
    """
    next_date = (datetime.now() + timedelta(days=days)).date()
    return next_date
