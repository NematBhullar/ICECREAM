'''
This file contains helper functions to help test the database.
'''
from functools import wraps
from src.db import get_db
from src.db_models.report import Report
from src.db_models.sender import Sender

def transactional_test(func):
    '''
    It will undo all the stuffs to the database in the function.
    It is used for unit testing so that the tests will not affect each other
    and the test will not change the testing database persistently.
    '''
    @wraps(func)
    def transactional_func(*args, **kwargs):
        db = get_db()
        with db.atomic() as txn:
            func(*args, **kwargs)
            txn.rollback()
    return transactional_func

def clear_db(func):
    """
    clear the tables in the database after doing the function.
    It is used for system testing.
    """
    @wraps(func)
    def clear_after_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            db = get_db()
            db.close()
            Report.truncate_table()
            Sender.truncate_table(cascade=True)
    return clear_after_func
