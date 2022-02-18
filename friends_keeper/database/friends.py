"""Friend database schema definition."""
import json

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql.sqltypes import Boolean

from friends_keeper.database import base_database


class Friend(base_database):
    """Friend table schema definition.

    Args:
        base_database (sqlalchemy.orm.declarative_base): Declarative base from sqlalchemy.
    """

    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    nickname = Column(String, unique=True)
    relationship = Column(String, nullable=True)
    min_days = Column(Integer)
    max_days = Column(Integer)
    active = Column(Boolean, default=True)

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
            "name": self.name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "relationship": self.relationship,
            "active": self.active,
            "min_days": self.min_days,
            "max_days": self.max_days,
        }
        return dict_data

    def __repr__(self) -> str:
        """Representation of the table in string format.

        Returns:
            str: String representation of the table.
        """
        return f"Friend: {str(self.to_dict())}"
