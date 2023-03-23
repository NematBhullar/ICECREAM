"""
database helper functions
"""
from uuid import UUID
from src.db_models.report import Report

def store_report(report_id: UUID, sender: str,report: dict):
    """
    Store a communication report
    
    Arguments:
        report_id (string)   - Identification for the report
        sender (string)      - Sender's username
        report (dict)        - A dictionary containing the status (for 
                               sender), report identification and 
                               content of the report

    Return Value: None
    
    """
    Report.insert(id=report_id, sender=sender, report=report).execute()