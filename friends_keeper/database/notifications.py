"""Notification event database schema definition."""

import json

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from friends_keeper.constants import DATE_FORMAT
from friends_keeper.database import base_database


class NotificationEvent(base_database):
    """Notification events table schema definition.

    Args:
        base_database (sqlalchemy.orm.declarative_base): Declarative base from sqlalchemy.
    """

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    friend_id = Column(ForeignKey(("friends.id")))
    date = Column(Date)
    already_notified = Column(Boolean, default=False)

    def to_json(self) -> str:
        """JSON representation of the table.

        Returns:
            str: JSON representation of the table in string.
        """
        json_output = self.to_dict()
        return json.dumps(json_output, indent=2)

    def to_dict(self) -> dict:
        """Dictionary representation of the table.

        Returns:
            dict: Table representation.
        """
        dict_data = {
            "id": self.id,
            "friend_id": self.friend_id,
            "date": self.date.strftime(DATE_FORMAT),
            "already_notified": self.already_notified,
        }
        return dict_data

    def __repr__(self) -> str:
        """Representation of the table in string format.

        Returns:
            str: String representation of the table.
        """
        return f"NotificationEvent: {str(self.to_dict())}"
