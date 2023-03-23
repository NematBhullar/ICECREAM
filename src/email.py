"""
Functions for sending invoice via email
"""
import logging
from smtplib import SMTP_SSL, SMTPResponseException, SMTPException
import ssl
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

def send_email(sender_name: str, recipient: str, content: str, msg: str=None)\
    ->dict:
    """
    Sends an email to the recipient, containing the invoice
    
    Arguments:
        sender_name (string) - The sender's username
        recipients (str)     - The email address to which the email 
                               will be sent
        content (string)     - The UBL format of the invoice 
   
    Return Value:
        status (dictionary)  - A simple dictionary containing the 
                               status of the report   
    
    """
    logging.info("%s send invoice to %s", sender_name, recipient)
    
    load_dotenv('.env')
    from_email = os.environ["EMAIL_ADDRESS"]

    # create and set up MIMEMultipart object
    message = MIMEMultipart(from_email)
    message["From"] = from_email
    message["To"] = recipient
    message["Subject"] = f"Invoice from {sender_name}"
    message.attach(MIMEText(
        f"An invoice from {sender_name} is attached below." 
            if msg is None else msg,
        "plain"
    ))
    
    # set up attachment
    attachment = MIMEBase("application", "octect-stream")
    attachment.set_payload(content)
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        "attachment; filename=invoice.xml"
    )
    message.attach(attachment)

    # transfer message object to string
    text = message.as_string()

    ssl_context = ssl.create_default_context()
    
    with SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
        server.login(from_email, os.environ["EMAIL_PASSWORD"])
        try:
            server.sendmail(from_email, recipient, text)
        except SMTPResponseException as e:
            logging.error(e)
            error_code = e.smtp_code
            error_message = e.smtp_error
            return {
                "status": "fail",
                "smtp_error_code": error_code,
                "reason": error_message,
            }
        except SMTPException as e:
            logging.error(e)
            return {
                "status": "fail",
                "reason": str(e)
            }
    return {
        "status": "success",
    }
