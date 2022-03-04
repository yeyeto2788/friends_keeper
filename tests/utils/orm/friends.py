from unittest import mock

import pytest

from sqlalchemy.exc import SQLAlchemyError

from friends_keeper.exceptions import DatabaseError
from friends_keeper.utils.orm.friends import create_friend
from friends_keeper.utils.orm.friends import delete_friend
from friends_keeper.utils.orm.friends import get_all_friend_notifications
from friends_keeper.utils.orm.friends import get_all_friends
from friends_keeper.utils.orm.friends import get_friend
from friends_keeper.utils.orm.friends import get_friend_notifications_sent
from friends_keeper.utils.orm.friends import get_next_friend_notification


@mock.patch("friends_keeper.utils.orm.friends.Session")
def test_create_friend(session_mock, db_session):
    session_mock.return_value = db_session
    friend = create_friend(nickname="nickname1", min_days=1, max_days=3)
    assert friend.id == 1


@mock.patch("friends_keeper.utils.orm.friends.Session")
def test_create_friend_abnomal(session_mock):
    session_mock.return_value.__enter__.return_value.add.side_effect = SQLAlchemyError()
    try:
        create_friend(nickname="nickname1", min_days=1, max_days=3)
    except DatabaseError:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_friend(get_object_mock, friend_list):
    get_object_mock.return_value = friend_list
    id = 1
    friend = get_friend(friend_id=id)
    assert friend.id == (id - 1)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_friend_abnormal1(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_friend(friend_id=id)
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_friend_none(get_object_mock):
    get_object_mock.return_value = []
    id = 1
    friend = get_friend(friend_id=id)
    assert friend == None


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_all_friends(get_object_mock, friend_list):
    get_object_mock.return_value = friend_list
    friends = get_all_friends()
    assert len(friends) == 2


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_all_friends_inactive(get_object_mock, friend_list):
    get_object_mock.return_value = friend_list
    friends = get_all_friends(show_inactive=True)
    assert len(friends) == 2


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_all_friends_abnormal(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_all_friends()
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_next_friend_notification(get_object_mock, two_notifications):
    get_object_mock.return_value = two_notifications
    id = 1
    notification = get_next_friend_notification(friend_id=id)
    assert notification.friend_id == (id - 1)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_next_friend_notification_abnormal(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_next_friend_notification(friend_id=1)
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_next_friend_notification_none(get_object_mock):
    get_object_mock.return_value = []
    id = 1
    notification = get_next_friend_notification(friend_id=id)
    assert notification == None


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_all_friend_notifications(get_object_mock, two_notifications):
    get_object_mock.return_value = two_notifications
    notifications = get_all_friend_notifications(friend_id=id)
    assert len(notifications) == 2


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_all_friend_notifications_abnormal(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_all_friend_notifications(friend_id=1)
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_all_friend_notifications_none(get_object_mock):
    get_object_mock.return_value = []
    id = 1
    notifications = get_next_friend_notification(friend_id=id)
    assert notifications == None


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_friend_notifications_sent(get_object_mock, two_notifications):
    get_object_mock.return_value = two_notifications
    id = 1
    notifications = get_friend_notifications_sent(friend_id=id)
    assert len(notifications) == 2


@mock.patch("friends_keeper.utils.orm.friends.get_object_from_query")
def test_get_friend_notifications_sent_abnormal(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_friend_notifications_sent(friend_id=1)
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.delete_friend_notification")
@mock.patch("friends_keeper.utils.orm.friends.execute_query")
def test_delete_friend(execute_query_mock, delete_friend_notification):
    delete_friend_notification.return_value = True
    execute_query_mock.return_value = True
    result = delete_friend(friend_id=1)
    assert True == result


@mock.patch("friends_keeper.utils.orm.friends.delete_friend_notification")
@mock.patch("friends_keeper.utils.orm.friends.execute_query")
def test_delete_friend_abnormal(execute_query_mock, delete_friend_notification):
    delete_friend_notification.return_value = True
    execute_query_mock.side_effect = DatabaseError

    try:
        delete_friend(friend_id=1)
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.friends.delete_friend_notification")
def test_delete_friend_notification_false(delete_friend_notification):
    delete_friend_notification.return_value = False
    result = delete_friend(friend_id=1)
    assert False == result
