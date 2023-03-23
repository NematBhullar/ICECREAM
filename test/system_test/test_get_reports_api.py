"""
system tests for reports endpoint
"""
from http.client import OK, UNAUTHORIZED
from uuid import uuid4
from deepdiff import DeepDiff
from src.db_helpers import store_report
from ..config import BASE_ROUTE
from ..db_test_helper import clear_db
import requests

@clear_db
def test_get_report_success():
    token = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    }).json()['token']
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
    store_report(report_id, "USER", report)
    response = requests.get(BASE_ROUTE + f"reports/{report_id}", headers={
        "Authorization": f"Bearer {token}",
    })
    assert response.status_code == OK
    data = response.json()
    assert DeepDiff(data, report, ignore_order=True) == {}

@clear_db
def test_get_report_no_token():
    requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    })
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
    store_report(report_id, "USER", report)
    response = requests.get(BASE_ROUTE + f"reports/{report_id}")
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get('reason') is not None

@clear_db
def test_non_exist_report_id():
    token = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    }).json()['token']
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
    store_report(report_id, "USER", report)
    response = requests.get(BASE_ROUTE + f"reports/{str(uuid4())}", headers={
        "Authorization": f"Bearer {token}",
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get('reason') is not None

@clear_db
def test_invalid_token_get_report():
    requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    })
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
    store_report(report_id, "USER", report)
    wrong_token = "edfshgfsddfghjgfdfghfd"
    response = requests.get(BASE_ROUTE + f"reports/{str(uuid4())}", headers={
        "Authorization": f"Bearer {wrong_token}",
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get('reason') is not None

@clear_db
def test_get_report_accessing_others_report():
    token1 = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER1"
    }).json()['token']
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z1111111@ad.unsw.edu.au",
            "status": "success",
            "time": 21345678
	    }, {
	        "type": "email",
            "to": "z222222@ad.unsw.edu.au",
            "status": "success",
            "time": 123443256
	    }]
    }

    token2 = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER2"
    }).json()['token']
    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
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
    store_report(report1_id, "USER1", report1)
    store_report(report2_id, "USER2", report2)
    response = requests.get(BASE_ROUTE + f"reports/{report1_id}", headers={
        "Authorization": f"Bearer {token2}",
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get('reason') is not None
    response = requests.get(BASE_ROUTE + f"reports/{report2_id}", headers={
        "Authorization": f"Bearer {token1}",
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"
    assert data.get('reason') is not None

@clear_db
def test_multiple_users_get_own_report():
    token1 = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER1"
    }).json()['token']
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z1111111@ad.unsw.edu.au",
            "status": "success",
            "time": 21345678
	    }, {
	        "type": "email",
            "to": "z222222@ad.unsw.edu.au",
            "status": "success",
            "time": 123443256
	    }]
    }

    token2 = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER2"
    }).json()['token']
    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
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
    store_report(report1_id, "USER1", report1)
    store_report(report2_id, "USER2", report2)
    response = requests.get(BASE_ROUTE + f"reports/{report1_id}", headers={
        "Authorization": f"Bearer {token1}",
    })
    assert response.status_code == OK
    data = response.json()
    assert data['status'] == "success"
    assert DeepDiff(data, report1) == {}
    response = requests.get(BASE_ROUTE + f"reports/{report2_id}", headers={
        "Authorization": f"Bearer {token2}",
    })
    assert response.status_code == OK
    data = response.json()
    assert data['status'] == "success"
    assert DeepDiff(data, report2) == {}

@clear_db
def test_get_multiple_reports():
    token = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    }).json()['token']
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z1111111@ad.unsw.edu.au",
            "status": "success",
            "time": 21345678
	    }, {
	        "type": "email",
            "to": "z222222@ad.unsw.edu.au",
            "status": "success",
            "time": 123443256
	    }]
    }

    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
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
    store_report(report1_id, "USER", report1)
    store_report(report2_id, "USER", report2)
    response = requests.get(BASE_ROUTE + "reports", headers={
        "Authorization": f"Bearer {token}",
    })
    assert response.status_code == OK
    data = response.json()
    assert DeepDiff(data, [report1, report2], ignore_order=True) == {}

@clear_db
def test_invalid_token_get_reports():
    requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    })
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z1111111@ad.unsw.edu.au",
            "status": "success",
            "time": 21345678
	    }, {
	        "type": "email",
            "to": "z222222@ad.unsw.edu.au",
            "status": "success",
            "time": 123443256
	    }]
    }

    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
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
    store_report(report1_id, "USER", report1)
    store_report(report2_id, "USER", report2)
    response = requests.get(BASE_ROUTE + "reports", headers={
        "Authorization": "Bearer ewrtyutrewrtyuytr",
    })
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"

@clear_db
def test_no_token_get_reports():
    requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    })
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z1111111@ad.unsw.edu.au",
            "status": "success",
            "time": 21345678
	    }, {
	        "type": "email",
            "to": "z222222@ad.unsw.edu.au",
            "status": "success",
            "time": 123443256
	    }]
    }

    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
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
    store_report(report1_id, "USER", report1)
    store_report(report2_id, "USER", report2)
    response = requests.get(BASE_ROUTE + "reports")
    assert response.status_code == UNAUTHORIZED
    data = response.json()
    assert data['status'] == "fail"


@clear_db
def test_multiple_user_get_reports():
    token1 = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER1"
    }).json()['token']
    report1_id = uuid4()
    report1 = {
        "status": "success",
        "report_id": str(report1_id),
        "report": [{
            "type": "email",
            "to": "z1111111@ad.unsw.edu.au",
            "status": "success",
            "time": 21345678
	    }, {
	        "type": "email",
            "to": "z222222@ad.unsw.edu.au",
            "status": "success",
            "time": 123443256
	    }]
    }

    token2 = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER2"
    }).json()['token']
    report2_id = uuid4()
    report2 = {
        "status": "success",
        "report_id": str(report2_id),
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
    store_report(report1_id, "USER1", report1)
    store_report(report2_id, "USER2", report2)
    response = requests.get(BASE_ROUTE + "reports", headers={
        "Authorization": f"Bearer {token1}",
    })
    assert response.status_code == OK
    data = response.json()
    assert DeepDiff(data, [report1]) == {}
    response = requests.get(BASE_ROUTE + "reports", headers={
        "Authorization": f"Bearer {token2}",
    })
    assert response.status_code == OK
    data = response.json()
    assert DeepDiff(data, [report2]) == {}

@clear_db
def test_no_reports():
    token = requests.post(BASE_ROUTE + "sender", json={
        "username": "USER"
    }).json()['token']
    response = requests.get(BASE_ROUTE + "reports", headers={
        "Authorization": f"Bearer {token}",
    })
    data = response.json()
    assert data == []
