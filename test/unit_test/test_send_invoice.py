"""
unit test the functions for the send_invoice route
"""
import tempfile
from json import dumps
import pytest
from unittest.mock import ANY
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import BadRequest

from src.send_invoice import real_send_invoice, send_invoice
from ..db_test_helper import transactional_test

class FakeRequest:
    def __init__(self, files, form, header=None) -> None:
        self.files = files
        self.form = form
        self.header = header
    

def test_send_invoice_success(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    report = real_send_invoice("ICE_CREAM", [
        {
            "type": "email",
            "to": "abc@gmail.com"
        },
    ], "invoice")
    assert len(report) == 1
    assert report[0]['status'] == "success"
    assert report[0]['to'] == "abc@gmail.com"
    assert report[0]['type'] == "email"

def test_send_invoice_fail():
    report = real_send_invoice("ICE_CREAM", [
        {
            "type": "sftp",
            "to": "abc@unsw.edu.au"
        },
    ], "invoice")
    assert report[0]['status'] == "fail"
    assert report[0]['to'] == "abc@unsw.edu.au"
    assert report[0]['type'] == "sftp"
    assert report[0].get('reason') is not None

def test_multiple_send_invoice(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    report = real_send_invoice("ICE_CREAM", [
        {
            "type": "sftp",
            "to": "abc@unsw.edu.au"
        },
        {
            "type": "email",
            "to": "abc@gmail.com"
        },
    ], "invoice")
    assert report[0]['status'] == "fail"
    assert report[1]['status'] == "success"
    assert report[0].get("reason") is not None
    assert report[1].get("reason") is None



@transactional_test
def test_invoice_and_recipients_are_files(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_send_sms = mocker.patch('src.send_invoice.send_sms')
    mock_send_sms.return_value = {
        "status": "success"
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create files
    with open('example1.xml', 'rb') as example_file:
        invoice = example_file.read()
    invoice_tmp = tempfile.TemporaryFile()
    invoice_tmp.write(invoice)
    recipients_file = tempfile.TemporaryFile()
    recipients_str = dumps(
        [
            {
                "type": "sms",
                "to": "12345678"
            },
            {
                "type": "email",
                "to": "abc@gmail.com"
            },
        ]
    ).encode('utf-8')

    recipients_file.write(recipients_str)
    files = ImmutableMultiDict([
        ('invoice', invoice_tmp),
        ('recipients', recipients_file),
    ])
    invoice_tmp.seek(0)
    recipients_file.seek(0)

    # set files field in the request mock
    mock_request = FakeRequest(files, ImmutableMultiDict([]))
    
    report = send_invoice(mock_request)
    assert report['status'] == 'success'
    mock_send_email.assert_called_with(ANY, "abc@gmail.com", ANY, ANY)
    mock_send_sms.assert_called_with(ANY, '12345678', ANY)

    recipients_file.close()
    invoice_tmp.close()


@transactional_test
def test_invoice_and_recipients_are_text(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create form
    with open('example1.xml', 'rb') as example_file:
        invoice = example_file.read()

    recipients_str = dumps(
        [
            {
                "type": "email",
                "to": "abc@gmail.com"
            },
        ]
    )
    form = ImmutableMultiDict([
        ('recipients', recipients_str),
        ('invoice', invoice),
    ])

    files = ImmutableMultiDict([])

    mock_request = FakeRequest(files, form)
    
    report = send_invoice(mock_request)
    assert report['report'][0]['status'] == 'success'
    assert report['status'] == 'success'

@transactional_test
def test_invoice_file_recipients_text(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username.return_value = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create form and files
    with open('example1.xml', 'rb') as example_file:
        invoice = example_file.read()

    recipients_str = dumps(
        [
            {
                "type": "email",
                "to": "xyz@email.com"
            },
            {
                "type": "email",
                "to": "abc@gmail.com"
            },
        ]
    )
    form = ImmutableMultiDict([
        ('recipients', recipients_str),
    ])

    invoice_file = tempfile.TemporaryFile()
    invoice_file.write(invoice)
    files = ImmutableMultiDict([
        ('invoice', invoice_file),
    ])
    invoice_file.seek(0)

    mock_request = FakeRequest(files, form)

    report = send_invoice(mock_request)
    assert report['status'] == 'success'
    assert report['report'][0]['status'] == 'success'
    assert report['report'][1]['status'] == 'success'

    invoice_file.close()

@transactional_test
def test_missing_recipients(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username.return_value = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create form and files
    with open('example1.xml', 'rb') as example_file:
        invoice = example_file.read()

    form = ImmutableMultiDict([])

    invoice_file = tempfile.TemporaryFile()
    invoice_file.write(invoice)
    files = ImmutableMultiDict([
        ('invoice', invoice_file),
    ])
    mock_request = FakeRequest(files, form)
    invoice_file.seek(0)

    
    with pytest.raises(BadRequest):
        send_invoice(mock_request)
    
    invoice_file.close()


@transactional_test
def test_missing_invoice(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username.return_value = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create form and files
    recipients_str = dumps(
        [
            {
                "type": "sms",
                "to": "12345678"
            },
            {
                "type": "email",
                "to": "abc@gmail.com"
            },
        ]
    )
    form = ImmutableMultiDict([
        ('recipients', recipients_str),
    ])

    files = ImmutableMultiDict([])

    mock_request = FakeRequest(files, form)
    
    with pytest.raises(BadRequest):
        send_invoice(mock_request)


def test_invalid_recipient_no_type(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username.return_value = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create form and files
    with open('example1.xml', 'rb') as example_file:
        invoice = example_file.read()

    recipients_str = dumps(
        [
            {
                "to": "12345678"
            }
        ]
    )
    form = ImmutableMultiDict([
        ('recipients', recipients_str),
    ])

    invoice_file = tempfile.TemporaryFile()
    invoice_file.write(invoice)
    files = ImmutableMultiDict([
        ('invoice', invoice_file),
    ])
    mock_request = FakeRequest(files, form)
    invoice_file.seek(0)
    
    report = send_invoice(mock_request)
    assert report['status'] == 'success'
    assert report['report'][0]['status'] == 'fail'

    invoice_file.close()
    

def test_invalid_recipient_no_to(mocker):
    mock_send_email = mocker.patch('src.send_invoice.send_email')
    mock_send_email.return_value = {
        "status": "success",
    }
    mock_sender = mocker.patch('src.send_invoice.get_sender_from_request')
    mock_sender.return_value.username.return_value = "ICE_CREAM"
    mocker.patch('src.send_invoice.store_report')

    # create form and files
    with open('example1.xml', 'rb') as example_file:
        invoice = example_file.read()

    recipients_str = dumps(
        [
            {
                "type": "email",
            }
        ]
    )
    form = ImmutableMultiDict([
        ('recipients', recipients_str),
    ])

    invoice_file = tempfile.TemporaryFile()
    invoice_file.write(invoice)
    files = ImmutableMultiDict([
        ('invoice', invoice_file),
    ])
    invoice_file.seek(0)

    mock_request = FakeRequest(files, form)
    
    report = send_invoice(mock_request)
    assert report['status'] == 'success'
    assert report['report'][0]['status'] == 'fail'

    invoice_file.close()