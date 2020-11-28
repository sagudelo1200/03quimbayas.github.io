#!/usr/bin/env python3
'''  '''
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel():
    ''' '''
    _class_ = ""
    id = ""
    created_at = ""
    date = ""
    hour = ""
    img_url = ""
    place = ""
    status = ""
    title = ""
    updated_at = ""

    def __init__(self, **kwargs):
        ''' Initialization of the base model '''
        for key, value in kwargs.items():
            if key != '__class__':
                setattr(self, key, value)
        if kwargs.get('created_at') and type(self.created_at) is str:
            self.created_at = datetime.strptime(kwargs['created_at'], time)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') and type(self.updated_at) is str:
            self.updated_at = datetime.strptime(kwargs['updated_at'], time)
        else:
            self.updated_at = datetime.utcnow()
        if not kwargs.get('id'):
            self.id = str(uuid4()).replace('-', '')[0:20]


    def __str__(self):
        '''String representation of the BaseModel class'''
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)
