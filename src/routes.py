'''
This file is the where we implement all the apis.
'''

from json import dumps
from flask import request, Blueprint
from werkzeug.exceptions import BadRequest, Conflict

from src.auth import create_token, get_token_from_request_raises
from src.format_report import format_report
from src.health import health_check

from src.report import get_reports, get_report
from src.send_invoice import send_invoice

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/send_invoice', methods=['POST'])
def send_invoice_route():
    return format_report(
        send_invoice(request), request.args.get('report-format', 'json'))


@api_v1.route('/health', methods=['GET'])
def health_route():
    return dumps(health_check())


@api_v1.route('/sender', methods=['POST'])
def create_api_key_route():
    input_json = request.get_json()

    username = input_json.get("username")
    if username is None:
        raise BadRequest("no username is provided")
    
    token = create_token(username)
    if token is None:
        raise Conflict("An API key is already created")
    
    return dumps({
        "status": "success",
        "token": token
    })



@api_v1.route('/reports', methods=['GET'])
def get_reports_route():
    report_format = request.args.get('report-format', 'json')
    token = get_token_from_request_raises(request)
    report_dict = get_reports(token)
    return format_report(report_dict, report_format)


@api_v1.route('/reports/<report_id>', methods=['GET'])
def get_report_route(report_id):
    token = get_token_from_request_raises(request)
    ret = get_report(token, report_id)
    return format_report(ret, request.args.get('report-format', 'json'))
