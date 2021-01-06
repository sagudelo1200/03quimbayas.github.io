#!/usr/bin/env python3
''' Base model for application objects '''
from datetime import datetime
from uuid import uuid4
from models import storage

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel():
    ''' Base model for application objects '''
    id = ""
    created_at = ""
    updated_at = ""

    def __init__(self, *args, **kwargs):
        ''' Initialization of the base model '''
        if kwargs:
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
                self.id = str(uuid4()).replace('-', '')[:20]
        else:
            self.id = str(uuid4()).replace('-', '')[:20]
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        '''String representation of the BaseModel class'''
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def to_dict(self, show_pwd=False):
        ''' Convert an object to its dict representation '''
        _dict = self.__dict__.copy()
        if 'created_at' in _dict:
            _dict['created_at'] = _dict['created_at'].strftime(time)
        if 'updated_at' in _dict:
            _dict['updated_at'] = _dict['updated_at'].strftime(time)
        _dict['__class__'] = self.__class__.__name__

        if not show_pwd:
            if 'hashed_pwd' in _dict:
                del _dict['hashed_pwd']
        return _dict

    def save(self):
        ''' Save obj in database '''
        self.updated_at = datetime.utcnow()
        doc = self.to_dict()
        doc['__class__'] = self.__tablename__

        storage.save(self.__tablename__, doc)

    def delete(self):
        ''' Delete obj from db '''
        if storage.exist(self.__tablename__, self.id):
            storage.delete(self.__tablename__, self.id)


if __name__ == "__main__":
    pass
