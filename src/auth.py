"""
Functions for authentication and authorization
"""
from peewee import IntegrityError
from hashlib import sha256
from secrets import token_urlsafe
from werkzeug.exceptions import Unauthorized
from src.db import get_db
from src.db_models.sender import Sender

def create_token(username: str) -> str:
    """
    Creates a token for the user and stores it in the Sender table
    If the username is already used, return None
    
    Arguments:
        username (string)    - User's login identification
   
    Return Value:
        token (string)       - A hashed key, given to each user 
    
    """
    token = token_urlsafe(64)
    hashed_token = hash_token(token)
    db = get_db()
    with db.atomic() as txn:
        try:
            Sender.create(username=username, token=hashed_token)
        except IntegrityError:
            txn.rollback()
            return None
    return token

def check_token_exists(token: str) -> bool:
    """
    Checks whether the token exists
    
    Arguments:
        token (string)       - A hashed key, given to each user
   
    Return Value:
        True, if the token exists
        False, otherwise
    
    """
    hashed_token = hash_token(token)
    return Sender.select().where(Sender.token == hashed_token).exists()

def get_sender_from_key(token: str) -> Sender:
    """
    Get the Sender object given the key
    If no such Sender, return None
    
    Arguments:
        token (string)       - A hashed key, given to each user    
    
    Return Value:
        sender (Sender)      - The sender associated with an invoice/
                               report    
    
    """
    hashed_token = hash_token(token)
    return Sender.get_or_none(Sender.token == hashed_token)

def get_token_from_request(request) -> str:
    """
    Gets the token string from the header of the request.
    Returns None if the there is no token in the header.
    
    Arguments:
        request 
    
    Return Value:
        token (string)       - A hashed key, given to each user  
    
    
    """
    value: str = request.headers.get("Authorization")

    if (value is not None) and (value.startswith("Bearer ")):
        return value[len("Bearer "):]
    else:
        return None

def get_token_from_request_raises(request) -> str:
    """
    Gets the token string from the header of the request.
    Throws an Unauthorized error if the there is no token in the header.
    
    Arguments:
        request 
    
    Return Value:
        token (string)       - A hashed key, given to each user      
    
    """

    ret = get_token_from_request(request)
    if ret is None:
        raise Unauthorized(
            "Please provide the API key in the header access the report."
        )
    return ret


def check_header_token(request):
    """
    It throws an Unauthorized error if there is no token in the header, 
    or the token is not in the database.
    
    Arguments:
        request 
    
    Return Value:
        None 
    
    """
    unathorized_error = Unauthorized(description=
        "You are unathorised." + 
        "Please make sure you provide a valid API key in the header."
    )
    token = get_token_from_request(request)
    if token is None:
        raise unathorized_error
    
    if not check_token_exists(token):
        raise unathorized_error

def get_sender_from_request(request):
    """
    Returns the Sender object of the token in the header.
    If there are no token or the token is not in the database, it throws an 
    Unauthorized error.
    
    Arguments:
        request 
    
    Return Value:
        sender (Sender)      - The sender associated with an invoice/
                               report 
    
    """
    token = get_token_from_request(request)
    unathorized_error = Unauthorized(
        "Please provide a valid API key in the header"
    )
    if token is None:
        raise unathorized_error
    sender = get_sender_from_key(token)
    if sender is None:
        raise unathorized_error
    return sender

def hash_token(token: str) -> str:
    """
    Helper function to hash the token
    
    Arguments:
        token (string)       - A string containing the user's key to 
                               authorise their access
    
    Return Value:
        token (string)       - A hashed key, given to each user 
    
    """
    return sha256(token.encode('utf-8')).hexdigest()

