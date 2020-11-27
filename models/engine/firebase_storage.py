#!/usr/bin/env python3
''' contains the firebase storage engine '''
import firebase_admin
from firebase_admin import credentials, firestore
from os import getenv

collections = ('Activities', )

cred = getenv('QUIMBAYAS_API_CREDENTIALS')


class FirebaseStorage:
    ''' performs queries and executes actions on the database '''
    __engine = None
    __db = None

    def __init__(self):
        ''' Validates the firebase sdk credentials and start de client '''

        try:
            if not cred:
                raise ValueError
            app = credentials.Certificate(cred)
            self.__engine = firebase_admin.initialize_app(app)
            self.__db = firestore.client()
        except Exception:
            raise ValueError(
                'QUIMBAYAS_API_CREDENTIALS: Invalid credentials or not found')

    def all(self, col=None):
        '''
        query on te current firestorage session and get all docs
        in the indicated collection or in all collections
        '''
        data = {}

        if col and col not in collections:
            return {'error': 400, 'message': f'Invalid collection ({col})'}

        for _col in collections:
            if not col or col == _col:
                docs = self.__db.collection(_col).stream()
                for doc in docs:
                    obj = doc.to_dict()
                    key = f'{_col}.{doc.id}'
                    obj['__class__'] = _col

                    id = obj.get('id')
                    if id and id != doc.id:
                        print(
                            f'[WARNING]: The document {key} contains an id',
                            f'field with a different value({id}) than its',
                            'actual id')
                    _class_ = obj.get('_class_')
                    if _class_ and _class_ != _col:
                        print(
                            f'[WARNING]: The document {key} contains an',
                            f'_class_ field with a different value({_class_})',
                            'than its actual collection')
                    if _class_:
                        obj.pop('_class_')
                    else:
                        print(
                            f'[WARNING]: The document {key} does not contain',
                            '_class_ field')

                    obj['id'] = doc.id
                    data[key] = obj

        return data

    def get(self, col, id):
        ''' Get doc from id in col '''
        doc = {}

        _col = self.all(col)
        if _col.get('error'):
            return _col

        doc = _col.get(f'{col}.{id}')

        if not doc:
            return {
                'error': 404,
                'message': f'the document <{id}> does not exist'}
        return doc

    def save(self, col, doc, merge=False):
        ''' Save in the database '''
        doc_ref = self.__db.collection(col).document(doc.get('id'))

        if doc.get('__class__'):
            doc['_class_'] = doc.get('__class__')
            doc.pop('__class__')

        doc_ref.set(doc, merge=merge)

    def delete(self, col, id):
        ''' Delete a document '''
        if col not in collections:
            return {'error': 400, 'message': f'Invalid collection ({col})'}
        doc_ref = self.__db.collection(col).document(id).delete()

    def count(self, col=None):
        ''' Counts documents '''
        return len(self.all(col))


if __name__ == "__main__":
    pass
