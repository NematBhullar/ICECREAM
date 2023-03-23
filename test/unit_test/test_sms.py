"""
test for sending invoice
"""
from unittest.mock import ANY
from src.sms import send_sms
from twilio.base.exceptions import TwilioRestException

def test_sms_success(mocker):
    client = mocker.patch('src.sms.Client')
    send_func = client.return_value.messages.create
    send_func.return_value.sid = "SM1234567890"
    res = send_sms("XYZ", "+15558675310", "message")
    assert res['status'] == "success"
    send_func.assert_called_with(to="+15558675310", body=ANY, from_=ANY)
    assert res['message_id'] == "SM1234567890"


def test_sms_exception(mocker):
    client = mocker.patch('src.sms.Client')
    send_func = client.return_value.messages.create
    send_func.side_effect = TwilioRestException("bad request", "xyz.com")
    res = send_sms("XYZ", "+15558675310", "message")
    assert res['status'] == "fail"
    assert 'reason' in res
    send_func.assert_called_with(to="+15558675310", body=ANY, from_=ANY)
