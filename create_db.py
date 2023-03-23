"""
This file is to initialize the database.
"""
from app_backend.models.recurring_invoice_model import RecurringInvoice
from src.db import get_db
from src.db_models.report import Report
from src.db_models.sender import Sender
import sys

def init_db(db):
    db.create_tables([Sender, Report, RecurringInvoice], safe=True)

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    database = get_db(arg)
    database.connect()
    init_db(database)
    database.close()
