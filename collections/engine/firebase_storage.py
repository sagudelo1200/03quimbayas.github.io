#!/usr/bin/env python3
''' contains the firebase storage engine '''
import firebase_admin
from firebase_admin import credentials, firestore
from os import getenv
from collections import collections

cred = getenv('QUIMBAYAS_API_CREDENTIALS')


class FirebaseStorage:
    ''' performs queries and executes actions on the database '''
    __engine = None
    __db = None

    def __init__(self):
        ''' Validates the firebase sdk credentials and start de client '''
        if not cred:
            print('QUIMBAYAS_API_CREDENTIALS: Invalid doc or not found')
            exit(-1)

        app = credentials.Certificate(cred)
        self.__engine = firebase_admin.initialize_app(app)
        self.__db = firestore.client()

    def all(self, col=None):
        '''
        query on te current firestorage session and get all docs
        in the indicated collection or in all collections
        '''
        data = {}

        if col and col not in collections:
            return {'error': f'Invalid collection ({col})'}

        for _col in collections:
            if not col or col == _col:
                try:
                    docs = self.__db.collection(_col).stream()

                    for doc in docs:
                        obj = doc.to_dict()
                        key = f'{_col}.{doc.id}'

                        id = obj.get('id')
                        if id and id != doc.id:
                            print(f'The document {key} contains an id field with a different value ({id}) than its actual id')

                        obj['id'] = doc.id
                        data[key] = obj
                except Exception as e:
                    print(e)

        return data


if __name__ == "__main__":
    db = DBStorage()

    print(db.all())
