from datetime import datetime

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from friends_keeper.constants import DEFAULT_CONFIGURATION
from friends_keeper.database import base_database
from friends_keeper.database.friends import Friend
from friends_keeper.database.notifications import NotificationEvent


@pytest.fixture(scope="session")
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine("sqlite://", echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def tables(db_engine):
    base_database.metadata.create_all(db_engine)
    try:
        yield
    finally:
        base_database.metadata.drop_all(db_engine)


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture
def db_session(db_engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = db_engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture
def normal_dumb_config():
    config = DEFAULT_CONFIGURATION
    return config


@pytest.fixture
def two_notifications():
    notifications = list()

    for index in range(0, 2):
        notifications.append(NotificationEvent(id=index, friend_id=index, date=datetime.now().date()))

    return notifications


@pytest.fixture
def friend_list():
    friends = []

    for index in range(0, 2):
        friends.append(Friend(id=index, nickname=f"nickname{index}", min_days=2, max_days=4, active=True))

    return friends


@pytest.fixture
def friend_by_index():
    index = 1
    return Friend(id=index, nickname=f"nickname{index}", min_days=2, max_days=4, active=True)
