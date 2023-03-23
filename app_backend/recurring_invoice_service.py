"""
implement the background process that poll the recurring invoices periodically 
to send them to the recipients
"""
import sys
import traceback
from typing import List
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import sleep
import logging
from peewee import PeeweeException
from app_backend.config import setup_variables

from app_backend.models.recurring_invoice_model import RecurringInvoice
from app_backend.send_invoice import send_invoice

from src.db import get_db

def poll_scheduled_invoices():
    try:
        ret = RecurringInvoice.select().where(
            RecurringInvoice.scheduled_time <= datetime.now())
    except PeeweeException:
        logging.error("fail to poll from the database")
        return []
    return ret


def send_scheduled_invoices(recurring_invoices: List[RecurringInvoice]):
    for schedule_invoice in recurring_invoices:
        today_str = str(date.today())
        due_date = schedule_invoice.scheduled_time + schedule_invoice.due_period
        uid = schedule_invoice.uid
        recipient = schedule_invoice.recipient
        invoice_data = schedule_invoice.invoice_data.copy()
        invoice_data['PaymentID'] = invoice_data['PaymentID'] + '/' + today_str
        invoice_data['IssueDate'] = today_str
        invoice_data['DueDate'] = due_date.strftime("%Y-%m-%d")

        # send invoice
        send_invoice(uid, recipient, invoice_data)

        # update recurring invoice
        set_next_scheduled_time(schedule_invoice)

def set_next_scheduled_time(recurring_invoice: RecurringInvoice):
    next_time = get_next_time(recurring_invoice)
    if next_time is not None:
        recurring_invoice.scheduled_time = next_time
        try:
            recurring_invoice.save()
        except PeeweeException:
            logging.error("error occurs when updating schedule_time")
    

def get_next_time(recurring_invoice: RecurringInvoice):
    intrval_map = {
        "m": lambda freq: timedelta(minutes=freq),
        "D": lambda freq: timedelta(days=freq),
        "W": lambda freq: timedelta(weeks=freq),
        "M": lambda freq: relativedelta(months=freq),
        "Y": lambda freq: relativedelta(years=freq),
    }

    get_delta = intrval_map.get(recurring_invoice.interval)
    if get_delta is None:
        logging.error("recurring invoice interval is invalid")
        return None

    return recurring_invoice.scheduled_time + \
        get_delta(recurring_invoice.frequency)


if __name__ == "__main__":
    # connect to database
    get_db()
    setup_variables()
    while True:
        # pylint: disable=bare-except
        try:
            scheduled_invoices = poll_scheduled_invoices()
            send_scheduled_invoices(scheduled_invoices)
        except:
            # make sure this process will not be terminated by exceptions
            logging.error("Unexpected error: %s", str(sys.exc_info()))
            traceback.print_stack()

        # sleep half a minute to be safe
        sleep(30)
