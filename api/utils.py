import hashlib
import binascii
import os

import datetime
import jwt

from config import Config


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                        salt, 100000)
    password_hash = binascii.hexlify(password_hash)
    return (salt + password_hash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    password_hash = hashlib.pbkdf2_hmac('sha512',
                                        provided_password.encode('utf-8'),
                                        salt.encode('ascii'),
                                        100000)
    password_hash = binascii.hexlify(password_hash).decode('ascii')

    return password_hash == stored_password


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=15),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, Config.SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'



