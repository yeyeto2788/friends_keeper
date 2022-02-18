"""Database declaration objects.

Raises:
    DatabaseError: If not able to connect the database.
"""
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from friends_keeper.exceptions import DatabaseError


# TODO: Decide whether this should be here on in 'extensions' module

# declarative base class
base_database = declarative_base()


try:
    # engine = create_engine("sqlite:///./friends_keeper.db", echo=True)
    engine = create_engine("sqlite:///./friends_keeper.db")

except TypeError:
    raise DatabaseError("Seems like database provided does not work :(\nPlease check you configuration.")

# Create a 'reusable' session object
Session = sessionmaker(expire_on_commit=False)
# Session.configure(bind=create_engine("sqlite:///./friends_keeper.db", echo=True))
Session.configure(bind=create_engine("sqlite:///./friends_keeper.db"))
