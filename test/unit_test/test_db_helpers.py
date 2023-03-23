"""
test the helper functions for database
"""
from uuid import uuid4
from src.db_models.report import Report
from src.db_models.sender import Sender
from src.db_helpers import store_report

from ..db_test_helper import transactional_test

@transactional_test
def test_store_report():
    Sender.create(username="ICE_CREAM", token="abcdef")
    report = {
        "abc": "123"
    }
    report_id = uuid4()
    store_report(report_id, "ICE_CREAM", report)
    assert Report.get_or_none(Report.id == report_id).report == report