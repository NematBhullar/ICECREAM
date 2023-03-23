"""
test the helper funcions provided in auth.py
"""
import pytest
from ..db_test_helper import transactional_test
from src.auth import (create_token, check_token_exists, get_sender_from_request, 
    get_token_from_request, get_sender_from_key, check_header_token, 
    get_token_from_request_raises)
from werkzeug.exceptions import Unauthorized


class _FlaskRequestMock:
    def __init__(self, headers) -> None:
        self.headers = headers


@transactional_test
def test_non_exist_token():
    assert not check_token_exists("abcdef")

@transactional_test
def test_token_created():
    token = create_token("ICECREAM")
    assert check_token_exists(token)

@transactional_test
def test_duplicated_username():
    create_token("ICE_CREAM")
    assert create_token("ICE_CREAM") is None

@transactional_test
def test_get_sender_from_key():
    token = create_token("ICE_CREAM")
    assert get_sender_from_key(token).username == 'ICE_CREAM'

@transactional_test
def test_hashed_token():
    token = create_token("ICE_CREAM")
    assert get_sender_from_key(token).token != token

@transactional_test
def test_no_sender_from_key():
    create_token("ICE_CREAM")
    assert get_sender_from_key("abcdef") is None

def test_get_header_token():
    token = "token"
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer " + token
    })
    assert get_token_from_request(request_mock) == token


def test_no_header_token():
    request_mock = _FlaskRequestMock({})
    assert get_token_from_request(request_mock) is None
    
    request_mock = _FlaskRequestMock({
        "Content-Type": "application/json"
    })
    assert get_token_from_request(request_mock) is None

    request_mock = _FlaskRequestMock({
        "Authorization": "Beerer token"
    })
    assert get_token_from_request(request_mock) is None

def test_get_header_token_raises():
    token = "token"
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer " + token
    })
    assert get_token_from_request_raises(request_mock) == token


def test_no_header_token_raises():
    request_mock = _FlaskRequestMock({})
    with pytest.raises(Unauthorized):
        get_token_from_request_raises(request_mock)
    
    request_mock = _FlaskRequestMock({
        "Content-Type": "application/json"
    })
    with pytest.raises(Unauthorized):
        get_token_from_request_raises(request_mock)

    request_mock = _FlaskRequestMock({
        "Authorization": "Beerer token"
    })
    with pytest.raises(Unauthorized):
        get_token_from_request_raises(request_mock)

@transactional_test
def test_check_header_token_no_token():
    request_mock = _FlaskRequestMock({})
    with pytest.raises(Unauthorized):
        check_header_token(request_mock)
    
    request_mock = _FlaskRequestMock({
        "Content-Type": "application/json"
    })
    with pytest.raises(Unauthorized):
        check_header_token(request_mock)

    request_mock = _FlaskRequestMock({
        "Authorization": "Beerer token"
    })
    with pytest.raises(Unauthorized):
        check_header_token(request_mock)

@transactional_test
def test_check_header_token_not_exists():
    create_token("user")
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer token"
    })
    with pytest.raises(Unauthorized):
        check_header_token(request_mock)
    
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer "
    })
    with pytest.raises(Unauthorized):
        check_header_token(request_mock)

@transactional_test
def test_check_header_token_no_except():
    token = create_token("ICE_CREAM")
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer " + token
    })
    # no error
    check_header_token(request_mock)

@transactional_test
def test_get_sender_from_request_no_auth_header():
    create_token("ICE_CREAM")
    request_mock = _FlaskRequestMock({})
    with pytest.raises(Unauthorized):
        get_sender_from_request(request_mock)

@transactional_test
def test_get_sender_from_request_wrong_token():
    token = create_token("ICE_CREAM")
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer " + token[:-1]
    })
    with pytest.raises(Unauthorized):
        get_sender_from_request(request_mock)

@transactional_test
def test_get_sender_from_request_success():
    token = create_token("ICE_CREAM")
    request_mock = _FlaskRequestMock({
        "Authorization": "Bearer " + token
    })
    # no exceptions
    assert get_sender_from_request(request_mock) is not None