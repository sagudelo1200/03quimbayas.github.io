#!/usr/bin/env python3
'''
initialize the collections package
'''
from os import getenv

type_storage = getenv('QUIMBAYAS_TYPE_STORAGE')

if type_storage == 'fb':
    from models.engine.firebase_storage import FirebaseStorage
    storage = FirebaseStorage()
else:
    raise TypeError('QUIMBAYAS_TYPE_STORAGE not valid')


def from_dict(source):
    ''' '''
    from models.activity import Activity

    obj = None

    activities = {'Activities': Activity}

    _class = source.get('_class_') or source.get('__class__')

    if _class in activities:
        obj = activities[_class](**source)

    return obj
