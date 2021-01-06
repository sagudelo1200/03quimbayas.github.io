#!/usr/bin/env python3
''' Representation of activity '''
from models.base_model import BaseModel
from datetime import timedelta


class Activity(BaseModel):
    ''' Representation of activity '''
    date = ''
    __tablename__ = 'Activities'
    active = False

    def __init__(self, *args, **kwargs):
        ''' initializes activity '''
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    pass
