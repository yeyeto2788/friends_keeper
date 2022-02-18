#!/usr/bin/env python3
from friends_keeper.database import base_database
from friends_keeper.database import engine
from friends_keeper.utils.orm.friends import create_friend


base_database.metadata.create_all(engine)

START_ID = 1001
END_ID = 1010


def create_test_friends():
    friends = list()

    for id in range(START_ID, END_ID + 1):
        friend = create_friend(
            name=f"name_{id}",
            last_name=f"lastname_{id}",
            nickname=f"nickname_{id}",
            min_days=9,
            max_days=14,
        )
        friends.append(friend)

    return friends


if __name__ == "__main__":
    create_test_friends()
