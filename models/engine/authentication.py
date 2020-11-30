#!/usr/bin/env python3
''' contains the authentication engine '''
from hashlib import pbkdf2_hmac as hash_pwd
from models import storage
import os


class Auth():
    ''' handles users authentication '''
    pass

    def get_user(self, id): return storage.get_user(id)

    def register(self, username, password):
        ''' Create a new user '''
        salt = os.urandom(14)
        hashed_pwd = hash_pwd('sha256', password.encode('utf-8'), salt, 100000)

        user = {
            'id': username,
            'username': username,
            'hashed_pwd': salt + hashed_pwd
        }

        storage.save('Users', user)

    def verify_password(self, stored_password, password):
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


auth = Auth()


if __name__ == "__main__":
    pass
