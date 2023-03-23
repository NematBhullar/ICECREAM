"""
function to initialize database
"""
import os
from dotenv import load_dotenv
from playhouse.postgres_ext import PostgresqlExtDatabase


_db = None

def get_db(database: str = None):
    global _db
    
    if _db is not None:
        return _db
    load_dotenv('.env')
    db_name = os.getenv('RDS_DB_NAME') if database is None else database
    db_user = os.getenv('RDS_USERNAME')
    db_host = os.getenv('RDS_HOSTNAME')
    db_port = os.getenv('RDS_PORT')
    db_password = os.getenv('RDS_PASSWORD')

    _db = PostgresqlExtDatabase(
            database=db_name,
            user=db_user,
            host=db_host,
            port=int(db_port),
            password=db_password,
            autorollback=True
        )
    return _db