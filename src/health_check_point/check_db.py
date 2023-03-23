"""
check the health of the database
"""
from peewee import DatabaseError
from src.db import get_db

def check_db_live():
    """
    Return Value:
        liveness (str)          - whether the the server can connect to the
                                  database
    """
    db = get_db()
    if db.is_connection_usable():
        return "up"
    try:
        db.connect()
    except DatabaseError:
        return "down"
    finally:
        db.close()
    return "up"
