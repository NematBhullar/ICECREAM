"""
The entry point
"""

import logging
import os
from flask import Flask, render_template
from flask_cors import CORS
from src.routes import api_v1
from src.config import SERVER_PORT
from src.db import get_db
from json import dumps
from dotenv import load_dotenv

from app_backend.route import app

def default_handler(err):
    response = err.get_response()
    logging.exception("response %s", err)
    response.data = dumps({
        "status": "fail",
        "code": err.code,
        "reason": str(err),
    })
    response.content_type = 'application/json'
    return response


application = Flask(__name__)
CORS(application)
application.config['TRAP_HTTP_EXCEPTION'] = True
application.register_error_handler(Exception, default_handler)

application.register_blueprint(api_v1, url_prefix='/api/v1')

application.register_blueprint(app, url_prefix='/app')

@application.route('/', methods=['GET'])
def index():
    return 'SENG2021_T131A_ICECREAM'

@application.route('/api/v1/docs')
def get_docs():
    return render_template('swaggerui.html')

if __name__ == '__main__':
    # load .env file
    load_dotenv(".env")
    
    db = get_db()

    if os.getenv('BUILD') in ('DEBUG', 'TEST'):
        application.run(port=SERVER_PORT)
    else:
        application.run(port=8000, debug=False)
