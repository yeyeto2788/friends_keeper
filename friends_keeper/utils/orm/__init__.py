"""ORM common utils functions module."""
import logging

from sqlalchemy.exc import SQLAlchemyError

from friends_keeper.database import Session
from friends_keeper.exceptions import DatabaseError


logger = logging.getLogger(__name__)


def execute_query(query) -> bool:
    """Execute given query against the database.

    Args:
        query (sqlalchemy.selectable): SQL query built with sqlalchemy.

    Raises:
        DatabaseError: Raised when executing query against database

    Returns:
        bool: Transaction result.
    """
    with Session() as session:
        try:
            logger.debug(f"Executing query: '{str(query)}'")
            session.execute(query)
            logger.debug(f"Commiting query: '{str(query)}'")
            session.commit()

        except SQLAlchemyError:
            msg = f"An error occurred executing query: '{str(query)}'"
            logger.error(msg)
            session.rollback()
            raise DatabaseError(msg)

        else:
            logger.debug("Query committed!")
            return True


def get_object_from_query(query) -> list:
    """Get objects from database based on given query.

    Args:
        query (sqlalchemy.selectable): SQL query built with sqlalchemy.

    Raises:
        DatabaseError: Raised when executing query against database

    Returns:
        list: List of objects gotten from executing query.
    """
    with Session() as session:
        try:
            logger.debug(f"Executing query: '{str(query)}'")
            result = session.execute(query).scalars().all()

        except SQLAlchemyError:
            msg = f"An error occurred getting object(s) from query: '{str(query)}'"
            logger.error(msg)
            session.rollback()
            raise DatabaseError(msg)

        else:
            logger.debug("Query executed!")
            return result
