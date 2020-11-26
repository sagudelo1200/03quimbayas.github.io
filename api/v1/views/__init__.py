#!/usr/bin/env python3
''' Blueprint of API '''
from flask import Blueprint

app_endpoints = Blueprint('app_endpoints', __name__, url_prefix='/')

from api.v1.views.activities import *
