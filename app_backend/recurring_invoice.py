"""
provide simple operations for recurring invoices
"""
from datetime import date, datetime, timedelta
from peewee import IntegrityError, PeeweeException
from playhouse.shortcuts import model_to_dict
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, \
    Forbidden
from app_backend.models.recurring_invoice_model import RecurringInvoice
from app_backend.send_invoice import create_invoice

from src.db import get_db

def create(uid, req_json: dict):
    db = get_db()
    try:
        recipient = req_json.pop("recipient")
        freq = req_json.pop("frequency")
        frequency = int(freq[:-1])
        interval = freq[-1]
        scheduled_date = get_scheduled_date(req_json['IssueDate'])
        due_date = str_to_date(req_json["DueDate"])
        due_period = get_due_period(due_date, scheduled_date)
    except KeyError as ke:
        raise BadRequest(f"missing key '{ke.args[0]}' in the json") from ke
    except ValueError as ve:
        raise BadRequest(f"invalid value in the json: {str(ve)}") from ve

    # check if the data are valid to create invoice
    err, _ = create_invoice(req_json)
    if err is not None:
        return err

    with db.atomic() as txn:
        try:
            recurring_invoice = RecurringInvoice.create(
                uid=uid, invoice_data=req_json, frequency=frequency, 
                interval=interval, recipient=recipient, due_period=due_period,
                scheduled_time=scheduled_date, 
            )
        except IntegrityError as ie:
            txn.rollback()
            raise Conflict("conflicts with the database") from ie

    return {
        "recurring_invoice_id": str(recurring_invoice.id),
        "code": 200,
        "status": "success"
    }

def get_list(uid):
    try:
        ret = RecurringInvoice.select().where(
            RecurringInvoice.uid == uid
        ).dicts()
    except PeeweeException as pe:
        raise InternalServerError("errors occur when querying the database") \
            from pe
    return {
        "status": "success",
        "code": 200,
        "recurring_invoices": ret,
    }

def get(uid, recurring_invoice_id):
    try:
        ret: RecurringInvoice = RecurringInvoice.get_or_none(
            RecurringInvoice.id == recurring_invoice_id)
    except PeeweeException as pe:
        raise InternalServerError("errors occur when querying the database") \
            from pe

    if (ret is None) or (str(ret.uid) != uid):
        raise Forbidden("cannot access the recurring invoice with id" + 
            f"{recurring_invoice_id}")
    return {
        "status": "success",
        "code": 200,
        "recurring_invoice": model_to_dict(ret),
    }

def delete(uid, recurring_invoice_id):
    uid = str(uid)
    try:
        n_deleted = RecurringInvoice.delete().where(
            (RecurringInvoice.uid == uid) & 
            (RecurringInvoice.id == recurring_invoice_id)).execute()
    except PeeweeException as pe:
        raise InternalServerError("errors occur when deleting the data") from \
            pe
    if n_deleted == 0:
        raise Forbidden(f"user with uid {uid} does not own a recurring" +\
                f"invoice with id {recurring_invoice_id}")
    return {
        "status": "success",
    }

def get_scheduled_date(issue_date_str):
    scheduled_date = str_to_date(issue_date_str)
    today = date.today()
    today_with_time = datetime(
        year=today.year, 
        month=today.month,
        day=today.day,
    )
    if scheduled_date < today_with_time:
        raise BadRequest("IssueDate field must not be before today")
    elif scheduled_date == today_with_time:
        return datetime.now() + timedelta(minutes=1)
    return scheduled_date

def get_due_period(due_date: datetime, issue_date: datetime):
    if due_date < issue_date:
        raise BadRequest("DueDate must be before IssueDate")
    return due_date - issue_date

def str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")
