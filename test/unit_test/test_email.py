"""
test sending invoice through email
"""
from smtplib import SMTPRecipientsRefused, SMTPResponseException

from src.email import send_email

def test_send_email_success(mocker):
    mocker.patch('src.email.SMTP_SSL')
    ret = send_email("ICE_CREAM", "abc@gmail.com", "abcdefg")
    assert ret['status'] == "success"


def test_send_email_invalic_response(mocker):
    mocked_server = mocker.patch('src.email.SMTP_SSL')
    mocked_server.return_value.__enter__.return_value.sendmail.side_effect = (
        SMTPResponseException(12, "reason"))
    ret = send_email("ICE_CREAM", "abc@gmail.com", "123456")
    assert ret['status'] == "fail"
    assert ret["reason"] == "reason"
    assert ret['smtp_error_code'] == 12

def test_send_email_other_exceptions(mocker):
    mocked_server = mocker.patch('src.email.SMTP_SSL')
    mocked_server.return_value.__enter__.return_value.sendmail.side_effect = (
        SMTPRecipientsRefused(["abcd"]))
    ret = send_email("ICE_CREAM", "abc", "2134567")
    assert ret['status'] == "fail"
