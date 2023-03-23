"""
test health check function
"""
from peewee import DatabaseError
from src.health import health_check

def test_everything_is_alive(mocker):
    mock_db = mocker.patch('src.health_check_point.check_db.get_db')
    mock_db.return_value.is_connection_usable.return_value = True
    health = health_check()
    assert health['liveness'] == "up"
    assert health['database']['liveness'] == 'up'
    assert mock_db.is_connection_usable.called_once_with()


def test_db_is_down(mocker):
    mock_db = mocker.patch('src.health_check_point.check_db.get_db')
    mock_db.return_value.is_connection_usable.return_value = False
    mock_db.return_value.connect.side_effect = DatabaseError
    health = health_check()
    assert health['liveness'] == "up"
    assert mock_db.is_connection_usable.called_once_with()
    assert mock_db.connect.called_once_with()
    assert health['database']['liveness'] == 'down'

