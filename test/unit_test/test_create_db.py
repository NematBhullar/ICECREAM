'''
Testing whether the database is initialized as expected
'''
from datetime import datetime
from uuid import uuid4
from peewee import IntegrityError

import pytest
from create_db import init_db
from src.db import get_db
from src.db_models.report import Report
from src.db_models.sender import Sender
from ..db_test_helper import transactional_test
import json


@transactional_test
def test_tables_created():
    db = get_db()
    init_db(db)
    Sender.select().dicts()
    Report.select().dicts()

@transactional_test
def test_inserting_to_tables():
    db = get_db()
    init_db(db)
    senders = [
        {
            "username": "ICECREAM",
            "token": "asfdgsadfdfs",
        },
        {
            "username": "user",
            "token": "12345FES",
        }
    ]
    # check no exceptions
    Sender.insert_many(senders).execute()
    reports = [
        {
            "id": uuid4(),
            "sender": "ICECREAM",
            "report": json.dumps({
                "report": "afs;gjfd;g"
            })
        }
    ]
    # check no exceptions
    Report.insert_many(reports).execute()

@transactional_test
def test_select_from_tables():
    db = get_db()
    init_db(db)
    senders = [
        {
            "username": "ICECREAM",
            "token": "asfdgsadfdfs",
        },
        {
            "username": "user",
            "token": "12345FES",
        }
    ]
    Sender.insert_many(senders).execute()
    assert Sender.select().where(
            Sender.username == "ICECREAM"
        ).dicts()[0]['token'] == "asfdgsadfdfs"
    
    assert len(Sender.select().where(Sender.username == "XYZ").dicts()) == 0

    reports =  [
        {
            "id": uuid4(),
            "sender": "ICECREAM",
            "time": datetime.now(),
            "report": json.dumps({
                "report": "afs;gjfd;g"
            })
        }
    ]
    Report.insert_many(reports).execute()
    assert len(Report.select().dicts()) == 1

@transactional_test
def test_not_unique_sender():
    db = get_db()
    init_db(db)
    Sender.insert({
        "username": "ICECREAM",
        "token": "fdsgdhggfdsd"
    }).execute()
    with pytest.raises(IntegrityError) :
        Sender.insert({
            "username": "ICECREAM",
            "token": "1234567"
        }).execute()
    with pytest.raises(Exception):
        Sender.insert({
            "username": "xyz",
            "token": "fdsgdhggfdsd"
        }).execute()

@transactional_test
def test_default_report_values():
    db = get_db()
    init_db(db)
    Sender.insert({
        "username": "ICECREAM",
        "token": "sdfagasdfgd"
    }).execute()
    curtime = datetime.now()
    Report.insert({
        "sender": "ICECREAM",
        "report": json.dumps({
            "report": "egdfsfag"
        })
    }).execute()
    assert (Report.select().dicts()[0]['time'] - curtime).total_seconds() < 100
    assert Report.select().dicts()[0]['id'] is not None

@transactional_test
def test_donot_insert_username():
    db = get_db()
    init_db(db)
    with pytest.raises(Exception):
        Sender.insert({
            "token": "12345"
        }).execute()

@transactional_test
def test_donot_insert_token():
    db = get_db()
    init_db(db)
    with pytest.raises(Exception):
        Sender.insert({
            "username": "ICECREAM"
        }).execute()

@transactional_test
def test_donot_insert_report_sender():
    db = get_db()
    init_db(db)
    Sender.insert({
        "username": "ICECREAM",
        "token": "sdfagasdfgd"
    }).execute()

    with pytest.raises(Exception):
        Report.insert({
            "report": json.dumps({
                "report": [
                    1, 2, 3
                ]
            })
        }).execute()
    
@transactional_test
def test_donot_insert_report_content():
    db = get_db()
    init_db(db)
    Sender.insert({
        "username": "ICECREAM",
        "token": "sdfagasdfgd"
    }).execute()
    
    with pytest.raises(Exception):
        Report.insert({
            "sender": "ICECREAM"
        }).execute()
