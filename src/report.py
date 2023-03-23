"""
This file is for get_report and get_reports routes
"""
from peewee import JOIN
from werkzeug.exceptions import Unauthorized
from src.auth import hash_token
from src.db_models.report import Report
from src.db_models.sender import Sender

def get_reports(token):
    """
    Returns all report contents in a list format, which token has access to.
    If there are no reports then raise 401 Unauthorized error.
    
    Arguments:
        token (string)       - A hashed key, given to each user
   
    Return Value:
        reports (list)       - A list of all reports the user has 
                               access to    
    
    """
    # select report from Report
    # join Sender on report.sender == sender.username
    # where report.id == report_id sender.token == hashed_token(token);
    ret = (Report
        .select(Report.report)
        .join(Sender, join_type=JOIN.RIGHT_OUTER)
        .where(Sender.token == hash_token(token))
    )
    if len(ret) == 0:
        raise Unauthorized(
            "You are unathorised to read this report. "
            "Please make sure you provide the API key in the header to "
            "access the report."
        )
    return [item.report for item in ret if item.report is not None]

def get_report(token, report_id):
    """
    Returns report contents which token has access to, where the report 
    is specified by the report_id
    If there are no report then raise 401 Unauthorized error.
    
    Arguments:
        token (string)       - A hashed key, given to each user
        report_id (string)   - Identification for the report

    Return Value:
        report (dictionary)  - A dictionary containing the status (for 
                               sender), report identification and 
                               content of the report 
    
    """
    ret = (Report
        .select(Report.report)
        .join(Sender)
        .where(
            (Sender.token == hash_token(token)) &
            (Report.id == report_id)
        )
    )
    if len(ret) == 0:
        raise Unauthorized(
        "You are unathorised to read this report. "
        "Please make sure you provide the API key in the header to "
        "access the report."
    )
    return ret[0].report
