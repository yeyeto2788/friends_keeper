"""Third party objects to use over the application.

In this module are somehow those objects that need to be
in a separate module so we do not we a cyclic import error.
"""
import logging
import os

from friends_keeper.constants import LOGGING_PATH


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(name)s] - [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGGING_PATH, "friends_keeper.log")),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
