"""
system tests for create sender
"""
from src.auth import check_token_exists
from ..config import BASE_ROUTE
from ..db_test_helper import clear_db
import requests
from http.client import BAD_REQUEST, OK, CONFLICT

@clear_db
def test_create_successfully():
    response = requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM"
    })
    assert response.status_code == OK
    data = response.json()
    assert data["status"] == "success"
    token = data["token"]
    assert check_token_exists(token)


@clear_db
def test_no_username():
    response = requests.post(BASE_ROUTE + "sender", json={
        "user": "ICE_CREAM"
    })
    assert response.status_code == BAD_REQUEST
    data = response.json()
    assert data["status"] == "fail"
    assert data.get("reason") is not None

@clear_db
def test_duplicate_username():
    requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM",
    })
    response = requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM"
    })
    assert response.status_code == CONFLICT
    data = response.json()
    assert data["status"] == "fail"
    assert data.get("reason") is not None

@clear_db
def test_invalid_josn():
    response = requests.post(BASE_ROUTE + "sender", 
        headers={
            "Content-type": "application/json",
        },
        data='{"username":"ICE_CREAM"'
    )

    assert response.status_code == BAD_REQUEST
    data = response.json()
    assert data["status"] == "fail"
    assert data.get("reason") is not None
