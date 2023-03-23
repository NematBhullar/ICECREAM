'''
The Report Entity in the database
'''
from uuid import uuid4
import peewee as pw
from playhouse.postgres_ext import JSONField

from src.db_models.entity import Entity
from src.db_models.sender import Sender


class Report(Entity):
    id = pw.UUIDField(primary_key=True, default=uuid4)
    sender = pw.ForeignKeyField(Sender, null=False)
    report = JSONField(null=False)
    time = pw.DateTimeField(constraints=[pw.SQL('default current_timestamp')])
