from datetime import datetime
from unittest import mock

import pytest

from sqlalchemy.exc import SQLAlchemyError

from friends_keeper.exceptions import DatabaseError
from friends_keeper.utils.orm.notifications import create_notification
from friends_keeper.utils.orm.notifications import delete_friend_notification
from friends_keeper.utils.orm.notifications import delete_notification
from friends_keeper.utils.orm.notifications import get_coming_notifications
from friends_keeper.utils.orm.notifications import get_notification
from friends_keeper.utils.orm.notifications import get_today_notifications
from friends_keeper.utils.orm.notifications import mark_notification_as_done
from friends_keeper.utils.orm.notifications import update_notification_event_date


@mock.patch("friends_keeper.utils.orm.notifications.get_object_from_query")
def test_get_today_notifications(get_object_mock, two_notifications):
    get_object_mock.return_value = two_notifications
    notifications = get_today_notifications()
    assert len(notifications) == 2


@mock.patch("friends_keeper.utils.orm.notifications.get_object_from_query")
def test_get_today_notifications_abnormal(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_today_notifications()
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.notifications.Session")
def test_create_notification(session_mock, db_session):
    session_mock.return_value = db_session
    notification = create_notification(friend_id=1, date=datetime.today().date())
    assert notification.friend_id == 1
    assert notification.id == 1


@mock.patch("friends_keeper.utils.orm.notifications.Session")
def test_create_notification_abnormal(session_mock):
    session_mock.return_value.__enter__.return_value.add.side_effect = SQLAlchemyError()
    try:
        create_notification(friend_id=1, date=datetime.today().date())
    except DatabaseError:
        pass


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_update_notification_event_date(execute_query_mock):
    execute_query_mock.return_value = True
    result = update_notification_event_date(friend_id=1, new_date=datetime.today().date())
    assert True == result


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_update_notification_event_date_abnormal(execute_query_mock):
    execute_query_mock.side_effect = DatabaseError
    try:
        update_notification_event_date(friend_id=1, new_date=datetime.today().date())
    except DatabaseError:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_delete_notification(execute_query_mock):
    execute_query_mock.return_value = True
    result = delete_notification(notification_id=1)
    assert True == result


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_delete_notification_abnormal(execute_query_mock):
    execute_query_mock.side_effect = DatabaseError
    try:
        delete_notification(notification_id=1)
    except DatabaseError:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_delete_friend_notification(execute_query_mock):
    execute_query_mock.return_value = True
    result = delete_friend_notification(friend_id=1, delete_all=False)
    assert True == result


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_delete_friend_notification_all(execute_query_mock):
    execute_query_mock.return_value = True
    result = delete_friend_notification(friend_id=1, delete_all=True)
    assert True == result


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_delete_friend_notification_abnormal(execute_query_mock):
    execute_query_mock.side_effect = DatabaseError
    try:
        delete_friend_notification(friend_id=1, delete_all=False)
    except DatabaseError:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_mark_notification_as_done(execute_query_mock):
    execute_query_mock.return_value = True
    result = mark_notification_as_done(notification_id=1)
    assert True == result


@mock.patch("friends_keeper.utils.orm.notifications.execute_query")
def test_mark_notification_as_done_abnormal(execute_query_mock):
    execute_query_mock.side_effect = DatabaseError
    try:
        mark_notification_as_done(notification_id=1)
    except DatabaseError:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.notifications.get_object_from_query")
def test_get_coming_notifications(get_object_mock, two_notifications):
    get_object_mock.return_value = two_notifications
    notifications = get_coming_notifications()
    assert len(notifications) == 2


@mock.patch("friends_keeper.utils.orm.notifications.get_object_from_query")
def test_get_coming_notifications_abnormal(get_object_mock):
    get_object_mock.side_effect = DatabaseError
    try:
        get_coming_notifications()
    except DatabaseError:
        pass
    else:
        pytest.raises(DatabaseError)


@mock.patch("friends_keeper.utils.orm.notifications.get_object_from_query")
def test_get_notification(get_object_mock, two_notifications):
    get_object_mock.return_value = two_notifications
    id = 1
    notification = get_notification(notification_id=id)
    assert notification.id == (id - 1)


@mock.patch("friends_keeper.utils.orm.notifications.get_object_from_query")
def test_get_notification_abnormal(get_object_mock, two_notifications):
    get_object_mock.side_effect = DatabaseError
    try:
        get_notification(notification_id=1)
    except DatabaseError:
        pytest.raises(DatabaseError)
