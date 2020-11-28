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
    print('QUIMBAYAS_TYPE_STORAGE not valid')
    exit(-1)
