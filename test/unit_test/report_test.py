"""
This file contains tests for storing and accessing reports
"""

from uuid import uuid4

import pytest
from deepdiff import DeepDiff
from werkzeug.exceptions import Unauthorized

from src.auth import create_token
from ..db_test_helper import transactional_test
from src.report import get_report, get_reports
from src.send_invoice import store_report


@transactional_test
def test_check_report():
    sender_id = "ICE_CREAM"
    token = create_token(sender_id)
    report_id = uuid4()
    report = {
        "status": "success",
        "report_id": str(report_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    
    store_report(report_id, sender_id, report)
    assert DeepDiff(get_report(token, report_id), report) == {}



@transactional_test
def test_report_id_invalid():
    sender_id = "ICE_CREAM"
    token = create_token("ICE_CREAM")
    report_id = uuid4()
    report = {
        "status": "success",
        "report_id": str(report_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    store_report(report_id, sender_id, report)
    wrong_report_id = uuid4()
    with pytest.raises(Unauthorized):
        get_report(token, wrong_report_id)

@transactional_test
def test_invalid_token_get_report():
    username = "USER"
    create_token("USER")
    report_id = uuid4()
    report = {
        "status": "success",
        "report_id": str(report_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    store_report(report_id, username, report)
    wrong_token = "dastyew45erdgfhtrsfghte"
    with pytest.raises(Unauthorized):
        get_report(wrong_token, report_id)

@transactional_test
def test_multiple_user_get_report():
    token1 = create_token("USER1")
    token2 = create_token("USER2")
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    report2_id = uuid4()
    report2 = {
        "status": "fail",
        "report_id": str(report2_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z51111@ad.unsw.edu.au",
            "status": "fail",
            "reason": "xftrhg",
            "time": "1234"
	    }]
    }
    store_report(report1_id, "USER1", report1)
    store_report(report2_id, "USER2", report2)
    assert DeepDiff(get_report(token1, report1_id), report1) == {}
    assert DeepDiff(get_report(token2, report2_id), report2) == {}

@transactional_test
def test_access_others_report():
    token1 = create_token("USER1")
    token2 = create_token("USER2")
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    report2_id = uuid4()
    report2 = {
        "status": "fail",
        "report_id": str(report2_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z51111@ad.unsw.edu.au",
            "status": "fail",
            "reason": "xftrhg",
            "time": "1234"
	    }]
    }
    store_report(report1_id, "USER1", report1)
    store_report(report2_id, "USER2", report2)
    with pytest.raises(Unauthorized):
        get_report(token1, report2_id)
    with pytest.raises(Unauthorized):
        get_report(token2, report1_id)

@transactional_test
def test_reports_all():
    token = create_token("ICE_CREAM")
    report_id = uuid4()
    report = {
        "status": "success",
        "report_id": str(report_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    store_report(report_id, "ICE_CREAM", report)
    reports = get_reports(token)
    assert len(reports) == 1
    assert DeepDiff(reports[0], report) == {}

@transactional_test
def test_reports_all_multiple():
    token = create_token("ICE_CREAM")
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    report2_id = uuid4()
    report2 = {
        "status": "fail",
        "report_id": str(report2_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z51111@ad.unsw.edu.au",
            "status": "fail",
            "reason": "xftrhg",
            "time": "1234"
	    }]
    }
    store_report(report1_id, "ICE_CREAM", report1)
    store_report(report2_id, "ICE_CREAM", report2)
    reports = get_reports(token)
    assert len(reports) == 2
    assert DeepDiff(reports, [report1, report2], ignore_order=True) == {}

@transactional_test
def test_cant_get_others_reports():
    token1 = create_token("USER1")
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    token2 = create_token("USER2")
    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "fail",
            "reason": "no such email",
            "time": "1234dasfhg"
	    }]
    }
    store_report(report1_id, "USER1", report1)
    store_report(report2_id, "USER2", report2)
    reports1 = get_reports(token1)
    assert len(reports1) == 1
    assert DeepDiff(reports1, [report1]) == {}
    reports2 = get_reports(token2)
    assert len(reports2)
    assert DeepDiff(reports2, [report2]) == {}

@transactional_test
def test_invalid_token_get_reports():
    create_token("ICE_CREAM")
    report_id = uuid4()
    report = {
        "status": "success",
        "report_id": str(report_id),
        "report": [{
            "type": "email",
            "to": "z5555555@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }, {
	        "type": "email",
            "to": "z5666666@ad.unsw.edu.au",
            "status": "success",
            "time": "1234"
	    }]
    }
    store_report(report_id, "ICE_CREAM", report)
    wrong_token = str("ertsyhjfdszrergsrdahetag")
    with pytest.raises(Unauthorized):
        get_reports(wrong_token)

@transactional_test
def test_no_reports():
    token = create_token("ICE_CREAM")
    assert get_reports(token) == []
