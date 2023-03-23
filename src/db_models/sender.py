'''
The Sender Entity in the database
'''
import peewee as pw
from src.db_models.entity import Entity

class Sender(Entity):
    username = pw.TextField(primary_key=True)
    token = pw.TextField(null=False, unique=True, index=True)

