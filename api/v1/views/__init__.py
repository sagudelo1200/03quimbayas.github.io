#!/usr/bin/env python3
''' API Blueprint '''
from flask import Blueprint

app_endpoints = Blueprint('app_endpoints', __name__, url_prefix='/v1/')

from api.v1.views.activities import *
from api.v1.views.index import *
