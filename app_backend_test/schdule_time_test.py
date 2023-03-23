"""
testing for the getting the next scheduled time for RecurringInvoice
"""
from datetime import date, datetime, timedelta
from uuid import uuid1

from app_backend.recurring_invoice_service import get_next_time


def get_mock_recurring_invoice(mocker, ri_id, uid, invoice_data, frequency, 
        interval, due_period, recipient, scheduled_time):
    recurring_invoice = mocker.patch(
        "app_backend.recurring_invoice.RecurringInvoice").return_value
    recurring_invoice.id = ri_id
    recurring_invoice.uid = uid
    recurring_invoice.invoice_data = invoice_data
    recurring_invoice.frequency = frequency
    recurring_invoice.interval = interval
    recurring_invoice.due_period = due_period
    recurring_invoice.recipient = recipient
    recurring_invoice.scheduled_time = scheduled_time
    return recurring_invoice


def test_get_next_schedule_time_invalid(mocker):
    mock = get_mock_recurring_invoice(mocker, uuid1(), **{
        "uid": uuid1(),
        "invoice_data": "fsagfh;dsf",
        "frequency": 1,
        "interval": "X", # invalid interval
        "due_period": timedelta(days=2),
        "scheduled_time": date(2022, 4, 16),
        "recipient": "example@email.com",
    })
    assert get_next_time(mock) is None

def test_get_next_schedule_time_month(mocker):
    mock = get_mock_recurring_invoice(mocker, uuid1(), **{
        "uid": uuid1(),
        "invoice_data": "fsagfh;dsf",
        "frequency": 1,
        "interval": "M",
        "due_period": timedelta(days=2),
        "scheduled_time": date(2022, 4, 16),
        "recipient": "example@email.com",
    })
    assert get_next_time(mock) == date(2022, 5, 16)

def test_get_next_schedule_time_week(mocker):
    mock = get_mock_recurring_invoice(mocker, uuid1(), **{
        "uid": uuid1(),
        "invoice_data": "fsagfh;dsf",
        "frequency": 1,
        "interval": "W",
        "due_period": timedelta(weeks=2),
        "scheduled_time": date(2022, 4, 25),
        "recipient": "example@email.com",
    })
    assert get_next_time(mock) == date(2022, 5, 2)

def test_get_next_schedule_time_day(mocker):
    mock = get_mock_recurring_invoice(mocker, uuid1(), **{
        "uid": uuid1(),
        "invoice_data": "fsagfh;dsf",
        "frequency": 1,
        "interval": "D",
        "due_period": timedelta(weeks=2),
        "scheduled_time": date(2022, 4, 25),
        "recipient": "example@email.com",
    })
    assert get_next_time(mock) == date(2022, 4, 26)

def test_get_next_schedule_time_minute(mocker):
    mock = get_mock_recurring_invoice(mocker, uuid1(), **{
        "uid": uuid1(),
        "invoice_data": "fsagfh;dsf",
        "frequency": 1,
        "interval": "m",
        "due_period": timedelta(weeks=2),
        "scheduled_time": datetime(2022, 4, 30, 12, 21, 0),
        "recipient": "example@email.com",
    })
    assert get_next_time(mock) == datetime(2022, 4, 30, 12, 22, 0)
