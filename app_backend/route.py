"""
this provides a route to be called by the frontend to create and send invoices
"""
import os
import subprocess
from flask import request, Blueprint
from werkzeug.exceptions import BadRequest

from app_backend.auth import get_uid
from app_backend.config import setup_variables
from app_backend import recurring_invoice
from app_backend.send_invoice import send_invoice

app = Blueprint('app', __name__)

if os.getenv('BUILD') != 'TEST':
    # set up config variables
    setup_variables()
    
    @app.route('/send_invoice', methods=['POST'])
    def app_send_invoice():
        # authorize
        uid = get_uid(request)
        
        try:
            req_json = request.get_json()
            recipient = req_json.pop('recipient')
        except BadRequest as br:
            raise BadRequest("fail to read the json") from br
        except KeyError as ke:
            raise BadRequest("missing recipient key") from ke

        return send_invoice(uid, recipient, req_json)

    @app.route('/recurring_invoices', methods=['GET', 'POST'])
    def app_recurring_invoices():
        uid = get_uid(request)
        if request.method == "POST":
            try:
                req_json = request.get_json()
            except BadRequest as br:
                raise BadRequest("fail to read the json") from br
            return recurring_invoice.create(uid, req_json)
        else:
            return recurring_invoice.get_list(uid)


    @app.route('/recurring_invoices/<recurring_invoice_id>', 
        methods=['GET', 'DELETE'])
    def app_get_recurring_invoice(recurring_invoice_id):
        uid = get_uid(request)
        if request.method == "GET":
            return recurring_invoice.get(uid, recurring_invoice_id)
        else:
            return recurring_invoice.delete(uid, recurring_invoice_id)
    
    # start the service which poll recurring invoices in the background
    subprocess.Popen(["python3", "-m", "app_backend.recurring_invoice_service"])