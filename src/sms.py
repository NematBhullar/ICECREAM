"""
provides function to send sms
"""
import logging
from os import environ
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv('.env')
account_sid = environ.get('SMS_ACCOUNT_SID')
account_password = environ.get('SMS_TOKEN')
phone_num = environ.get('SMS_PHONENUM')

# phone number in e.164 format (https://www.twilio.com/docs/glossary/what-e164)

def send_sms(sender: str, to: str, message: str):
    client = Client(account_sid, account_password)
    try:
        sms = client.messages.create(
            to=to, 
            from_=phone_num,
            body=f"from {sender}:\n{message}"
        )
    except TwilioRestException as err:
        logging.error(err.__repr__())
        return {
            "status": "fail",
            "reason": err.__repr__(),
        }
    return {
        "status": "success",
        "message_id": sms.sid
    }
