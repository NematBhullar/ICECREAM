'''
Entity class as the base class for database models.
'''
from peewee import Model
from src.db import get_db

class Entity(Model):
    class Meta:
        database = get_db()
