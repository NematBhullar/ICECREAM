"""
implement functions that are useful for authenticating the user
"""
from werkzeug.exceptions import Unauthorized
from firebase_admin import auth

def get_token(req):
    auth_header = req.headers.get("Authorization")
    if (auth_header is not None) and (auth_header.startswith("Bearer ")):
        return auth_header[len("Bearer "):]
    else:
        raise Unauthorized("Please log in")

def get_uid(req):
    token = get_token(req)
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except auth.InvalidIdTokenError as e:
        raise Unauthorized('ID token is invalid, expired or revoked') from e
    