"""
implement the send_invoice function for /send_invoice endpoint in app_backend
"""
from firebase_admin import storage, db
import requests
from app_backend import config
from flask import Response
import json
from uuid import uuid1
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR
from datetime import date


def send_invoice(uid, recipient, invoice_data):
    # create invoice    
    err, invoice = create_invoice(invoice_data)
    if err is not None:
        return err

    # send invoice
    sender = invoice_data['SupplierRegistration']
    err, report = send_email_invoice(invoice, recipient, sender)
    if err is not None:
        return err

    store_invoice_url = store_invoice(uid, invoice, invoice_data, recipient)
    return Response(json.dumps({
        "invoice_url": store_invoice_url,
        "report": report,
    }), status=200, mimetype='application/json')


def create_invoice(invoice_data):
    try:
        res = requests.post(config.CREATE_INVOICE_URL, json=invoice_data)
    except requests.exceptions.ConnectionError:
        return Response(json.dumps({
            "report": {
                "status": "fail",
                "reason": "cannot connect to the create invoice server"
            }
        }), status=INTERNAL_SERVER_ERROR, mimetype='application/json'), None
    
    if (res.status_code != 200) or (not res.text.startswith("<?xml")):
        return Response(json.dumps({
            "report": {
                "status": "fail",
                "reason": f"invalid input for create invoice:\n{res.text}"
            }
        }), status=BAD_REQUEST, mimetype='application/json'), None
    return None, res.text


def send_email_invoice(invoice, recipient, sender):
    try:
        res = requests.post(config.SEND_INVOICE_URL, 
        files={
            "invoice": ("invoice.xml", invoice),
            "recipients": ("", json.dumps(
                [
                    {
                        "type": "email",
                        "to": recipient,
                        "sender": sender,
                    }
                ]
            ), "application/json")
        }, headers={
            "Authorization": "Bearer " + config.SEND_INVOICE_TOKEN,
        })
    except requests.exceptions.ConnectionError:
        return Response(json.dumps({
            "report": {
                "status": "fail",
                "reason": "cannot connect to the send invoice server"
            }
        }), status=500, mimetype='application/json'), None

    report = res.json()
    if (report['status'] == 'fail') or (
        report['report'][0]['status'] == 'fail'):
        return Response(json.dumps({
            "report": report
        }), status=BAD_REQUEST, mimetype='application/json'), None
    return None, report


def store_invoice(uid, invoice, meta_data, recipient_email):
    # assume firebase is alive, and no error checking
    # store invoice
    bucket = storage.bucket()
    invoice_id = uuid1()
    blob = bucket.blob(f"users/{uid}/invoices/{invoice_id}.xml")
    blob.upload_from_string(invoice)
    # url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

    db_ref = db.reference(f'/invoices/{uid}/{invoice_id}')
    db_ref.set({
        'url': blob.name,
        'paid': False,
        'payment_id': meta_data['PaymentID'],
        'create_date': date.today().isoformat(),
        'issue_date': meta_data['IssueDate'],
        'due_date': meta_data['DueDate'],
        'customer': meta_data['CustomerRegistration'],
        'recipient_email': recipient_email,
    })
    return blob.name
