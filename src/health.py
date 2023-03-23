"""
implement the health check function
"""

from src.health_check_point.check_db import check_db_live
from src.health_check_point.uptime import get_uptime


def health_check():
    """
    Return Value:
    health report (dictionary)         - the liveness field indicates whetther
                                        the server is alive. The database field 
                                        indicates the health status of the 
                                        database. The uptime indicates how long 
                                        the server has been alive.
    """
    return {
        "liveness": "up",
        "database": {
            "liveness": check_db_live(),
        },
        "uptime": str(get_uptime()),
    }
