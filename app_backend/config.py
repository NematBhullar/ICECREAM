"""
set up global variables based on configuration
"""
import firebase_admin
import os

firebase_app = None
SEND_INVOICE_URL = None
CREATE_INVOICE_URL = None
SEND_INVOICE_TOKEN = None

def setup_variables():
    global firebase_app
    global SEND_INVOICE_URL
    global CREATE_INVOICE_URL
    global SEND_INVOICE_TOKEN
    if os.getenv('BUILD') == 'DEBUG':
        cred_obj = firebase_admin.credentials.Certificate(
            './firebase_credentials.json')
        SEND_INVOICE_URL = 'http://127.0.0.1:8080/api/v1/send_invoice'
    else:
        cred_obj = firebase_admin.credentials.Certificate(
            '../firebase_cred.json')
        SEND_INVOICE_URL = 'https://www.seng2021g23.tk/api/v1/send_invoice'

    firebase_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL': os.environ['databaseURL'],
        'storageBucket': os.environ['storageURL']
    })
    CREATE_INVOICE_URL = ("https://seng-donut-deployment.herokuapp.com" + 
        "/json/convert")
    SEND_INVOICE_TOKEN = os.environ['SEND_INVOICE_TOKEN']
