"""
system tests for send_invoice route
"""
from http.client import BAD_REQUEST, OK, UNAUTHORIZED
import json
from uuid import uuid4
import requests
from ..config import BASE_ROUTE
from ..db_test_helper import clear_db

@clear_db
def test_send_invoice_no_authenitication_header():
    response = requests.post(BASE_ROUTE + "send_invoice", files={
        "invoice": ("", open("example1.xml", "rb")),
        "recipients": ("", json.dumps(
            [
                {
                    "type": "email",
                    "to": "abc@gmail.com"
                },
                {
                    "type": "sms",
                    "to": "231467"
                }
            ]
        ))
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get("reason") is not None

@clear_db
def test_send_invoice_invalid_token():
    assert requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM"
    }).status_code == OK

    response = requests.post(BASE_ROUTE + "send_invoice", files={
        "invoice": ("", open("example1.xml", "rb")),
        "recipients": ("", json.dumps(
            [
                {
                    "type": "email",
                    "to": "abc@gmail.com"
                },
                {
                    "type": "sms",
                    "to": "231467"
                }
            ]
        ), "application/json")
    }, headers={
        "Authorization": "Bearer " + str(uuid4()),
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get("reason") is not None

@clear_db
def test_send_invoice_invalid_json():
    response = requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM"
    })
    token = response.json()['token']

    response = requests.post(BASE_ROUTE + "send_invoice", files={
        "invoice": ("", open("example1.xml", "rb")),
        "recipients": ("", json.dumps(
            [
                {
                    "type": "email",
                    "to": "abc@gmail.com"
                },
                {
                    "type": "sms",
                    "to": "231467"
                }
            ]
        )[:-2], "application/json")
    }, headers={
        "Authorization": "Bearer " + token
    })
    assert response.status_code == BAD_REQUEST
    data = response.json()
    assert data['status'] == "fail"
    assert data.get("reason") is not None

@clear_db
def test_invalid_input():
    response = requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM"
    })
    token = response.json()['token']

    response = requests.post(BASE_ROUTE + "send_invoice", files={
        "invoice": open("example1.xml", "rb"),
        "xyz": ("", json.dumps(
            [
                {
                    "type": "email",
                    "to": "abc@gmail.com"
                },
                {
                    "type": "sms",
                    "to": "231467"
                }
            ]
        )[:-2], "application/json")
    }, headers={
        "Authorization": "Bearer " + token,
    })
    assert response.status_code == BAD_REQUEST
    data = response.json()
    assert data['status'] == "fail"
    assert data.get("reason") is not None

@clear_db
def test_not_multipart_input():
    response = requests.post(BASE_ROUTE + "sender", json={
        "username": "ICE_CREAM"
    })
    token = response.json()['token']
    with open("example1.xml", "r", encoding="utf_8") as invoice_file:
        invoice = invoice_file.read()
    response = requests.post(BASE_ROUTE + "send_invoice", json={
        "invoice": invoice,
        "recipients":
            [
                {
                    "type": "email",
                    "to": "abc@gmail.com"
                },
                {
                    "type": "sms",
                    "to": "231467"
                }
            ]
    }, headers={
        "Authorization": "Bearer " + token,
    })
    assert response.status_code == BAD_REQUEST
    data = response.json()
    assert data['status'] == "fail"
    assert data.get("reason") is not None

# This function cannot be run on GitHub as it requires email credentials
# @clear_db
# def test_send_invoice_success():
#     response = requests.post(BASE_ROUTE + "sender", json={
#         "username": "ICE_CREAM"
#     })
#     token = response.json()['token']
#     response = requests.post(BASE_ROUTE + "send_invoice", files={
#         "invoice": open("example1.xml", "rb"),
#         "recipients": ("", json.dumps(
#             [
#                 {
#                     "type": "email",
#                     "to": "abc@gmail.com"
#                 },
#                 {
#                     "type": "sms",
#                     "to": "231467"
#                 }
#             ]
#         ), "application/json")
#     }, headers={
#         "Authorization": "Bearer " + token,
#     })
#     assert response.status_code == OK
#     data = response.json()
#     assert data['status'] == "success"
