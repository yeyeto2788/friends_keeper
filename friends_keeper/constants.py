"""Constants used all over the application.

Most of the variables defined here are references for the actual
value within the `config.yaml` file.
"""
import os

from collections import namedtuple


__repo_root = os.path.dirname(os.path.dirname(__file__))
REPO_ROOT_DIR = __repo_root
CONFIGURATION_FILE_PATH = "./config.yaml"
LOGGING_PATH = os.path.abspath(__repo_root)

DATE_FORMAT = "%d/%m/%y"

__notifiers = {"file": "file", "gotify": "gotify", "email": "email"}
NOTIFIER_TYPES = namedtuple("directions", __notifiers.keys())(**__notifiers)
NOTIFICATIONS_FILE_PATH = os.path.join(REPO_ROOT_DIR, "notifications.txt")

ACTIONS = ["message", "call", "text"]
REMINDING_NOTES = [
    "I know you’re busy managing managing life, keeping friends is important so, {action} {friend_name}",
    "Just a friendly follow-up. Please, {action} {friend_name}",
    "Remember to {action} {friend_name}",
    "You need to {action} {friend_name}",
    "{action} {friend_name}",
    "Hey U! {action} {friend_name} NOW",
    "SOS!!!!\n{action} {friend_name}",
]

# TODO: Dump default configuration if no configuration file provided.
DEFAULT_CONFIGURATION = {
    "logging": {
        "path": os.path.join(
            REPO_ROOT_DIR,
            "friends_keeper.log",
        ),
        "debug_level": "ERROR",
    },
    "notifications": {
        "type": ["file"],
        "title": "Friends keeper notification",
    },
    "notifiers": {
        "file": {
            "path": os.path.join(
                REPO_ROOT_DIR,
                "notifications.txt",
            )
        }
    },
}


YAML_SCHEMA = {
    "type": "object",
    "properties": {
        "logging": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "debug_level": {"enum": ["DEBUG", "INFO", "ERROR", "NOTSET"]},
                "log_requests": {"type": "boolean"},
            },
            "required": ["path", "debug_level"],
        },
        "notifications": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "title": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["type"],
        },
        "notifiers": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                    },
                    "required": ["path"],
                },
                "gotify": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string"},
                        "app_token": {"type": "string"},
                        "client_token": {"type": "string"},
                        "create_app": {"type": "boolean"},
                    },
                    "required": ["url", "app_token"],
                },
                "email": {
                    "type": "object",
                    "properties": {
                        "port": {"type": "integer"},
                        "password": {"type": "string"},
                        "from_address": {"type": "string"},
                        "to_address": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["password", "from_address", "to_address"],
                },
                "telegram": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                    },
                    "required": ["token"],
                },
            },
        },
    },
}
