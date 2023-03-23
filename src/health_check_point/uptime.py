"""
functions to measure the uptime of server
"""
from datetime import datetime, timedelta

start_sever_time = datetime.utcnow()

def get_uptime() -> timedelta:
    """
    Return Value:
    uptime (timedelta)          - how long the server has been alive
    """
    return datetime.utcnow() - start_sever_time
