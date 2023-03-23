"""
testing for creating, getting and removing recurring invoices
"""
from flask import Response
from datetime import datetime, timedelta
from http.client import BAD_REQUEST
from uuid import uuid1
import json
from app_backend.recurring_invoice_service import poll_scheduled_invoices
from app_backend import recurring_invoice
from app_backend.models.recurring_invoice_model import RecurringInvoice
from test.db_test_helper import transactional_test
from werkzeug.exceptions import BadRequest, Forbidden
import pytest

@transactional_test
def test_create_success(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    ret = recurring_invoice.create(uuid1(), {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    assert ret['status'] == "success"
    invoice = RecurringInvoice.get_or_none()
    assert invoice.interval == "D"
    assert invoice.due_period == timedelta(days=14)

@transactional_test
def test_create_fail_missing_key(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    with pytest.raises(BadRequest):
        recurring_invoice.create(uuid1(), {
            "recipient": "example@email.com",
            "frequency": "1D",
            "IssueDate": "2024-04-17",
        })

@transactional_test
def test_create_fail_request_unsuccessful(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (Response(
        json.dumps({
            "report": {
                "status": "fail",
                "reason": "invalid input for create invoice:\n"
            }
        }), status=BAD_REQUEST, mimetype='application/json'
    ), None)
    ret = recurring_invoice.create(uuid1(), {
            "recipient": "example@email.com",
            "frequency": "1D",
            "IssueDate": "2024-04-17",
            "DueDate": "2024-05-01",
        })
    assert isinstance(ret, Response)
    assert ret.status_code == BAD_REQUEST

@transactional_test
def test_get_list(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    user1 = uuid1()
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1M",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    res = recurring_invoice.get_list(str(user1))
    assert res['status'] == "success"
    invoices_list = res['recurring_invoices']
    assert len(invoices_list) == 2
    assert datetime.strftime(invoices_list[0]['scheduled_time'], "%Y-%m-%d")\
         == "2024-04-17"

@transactional_test
def test_get_list_other_user(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    user1 = uuid1()
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1M",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    user2 = uuid1()
    res = recurring_invoice.get_list(str(user2))
    assert res['status'] == "success"
    assert res['recurring_invoices'] == []

@transactional_test
def test_get_one(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    user1 = uuid1()
    res = recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    invoice_id = res['recurring_invoice_id']
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1M",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    res = recurring_invoice.get(str(user1), invoice_id)
    assert res['status'] == "success"
    invoice = res['recurring_invoice']
    assert datetime.strftime(invoice['scheduled_time'], "%Y-%m-%d")\
         == "2024-04-17"

@transactional_test
def test_get_none(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    user1 = uuid1()
    res = recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    invoice_id = res['recurring_invoice_id']
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1M",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    with pytest.raises(Forbidden):
        res = recurring_invoice.get(str(uuid1()), invoice_id)

@transactional_test
def test_delete_fail(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    user1 = uuid1()
    res = recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    invoice_id = res['recurring_invoice_id']
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1M",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    with pytest.raises(Forbidden):
        res = recurring_invoice.delete("user2", invoice_id)
    res = recurring_invoice.get_list(str(user1))
    assert len(res["recurring_invoices"]) == 2

@transactional_test
def test_delete_success(mocker):
    create_req_mock = mocker.patch(
        "app_backend.recurring_invoice.create_invoice")
    create_req_mock.return_value = (None, "invoice in xml")
    user1 = uuid1()
    res = recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1D",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    invoice_id = res['recurring_invoice_id']
    recurring_invoice.create(user1, {
        "recipient": "example@email.com",
        "frequency": "1M",
        "IssueDate": "2024-04-17",
        "DueDate": "2024-05-01",
    })
    res = recurring_invoice.delete(str(user1), invoice_id)
    assert res['status'] == "success"
    res = recurring_invoice.get_list(str(user1))
    assert len(res["recurring_invoices"]) == 1


@transactional_test
def test_get_scheduled_invoices_empty():
    RecurringInvoice.create(uid="user1", invoice_data={"invoice": "data1"},
        frequency=1, interval="D", recipient="example@email.com", 
        due_period=timedelta(days=30), scheduled_time=(
            datetime.today() - timedelta(days=1))
    )
    RecurringInvoice.create(uid="user2", invoice_data={"invoice": "data2"},
        frequency=1, interval="D", recipient="example@email.com", 
        due_period=timedelta(days=30), scheduled_time=(
            datetime.today() - timedelta(days=1))
    )
    invoice_list = poll_scheduled_invoices()
    assert len(invoice_list) == 2
    assert invoice_list[0].uid in ("user1", "user2")
    assert invoice_list[1].uid in ("user1", "user2")

@transactional_test
def test_get_scheduled_invoices_list():
    RecurringInvoice.create(uid="user1", invoice_data={"invoice": "data1"},
        frequency=1, interval="D", recipient="example@email.com", 
        due_period=timedelta(days=30), scheduled_time=(
            datetime.today() + timedelta(days=1))
    )
    RecurringInvoice.create(uid="user2", invoice_data={"invoice": "data2"},
        frequency=1, interval="D", recipient="example@email.com", 
        due_period=timedelta(days=30), scheduled_time=(
            datetime.today() + timedelta(days=1))
    )
    invoice_list = poll_scheduled_invoices()
    assert len(invoice_list) == 0
