#!/usr/bin/env python3
''' contains the authentication engine '''
from hashlib import pbkdf2_hmac as hash_pwd
from models import storage
import os


def register(username, password):
    ''' Create a new user '''
    salt = os.urandom(14)
    hashed_pwd = hash_pwd('sha256', password.encode('utf-8'), salt, 100000)

    user = {
        'id': username,
        'username': username,
        'hashed_pwd': salt + hashed_pwd
    }

    storage.save('Users', user)


def verify_password(stored_password, password):
    ''' Verify password '''
    if not stored_password or not password:
        return False
    if type(stored_password) is not bytes or type(password) is not str:
        return False
    salt = stored_password[:14]
    hashed_password = stored_password[14:]

    hashed_pwd = hash_pwd('sha256', password.encode('utf-8'), salt, 100000)

    if hashed_pwd == hashed_password:
        return True
    return False


def identity(payload):
    print('____identity', end=" ")
    id = payload.get('identity')
    print(id)

    return storage.get_user(id)


def authenticate(username, password):
    print('____authenticate', end=" ")
    user = storage.get_user(username)
    print(user.id)

    if user and verify_password(user.get('hashed_pwd'), password):
        return user


if __name__ == "__main__":
    pass
