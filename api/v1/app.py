#!/usr/bin/env python3
''' RESTful API '''
from api.v1.tools.response import custom_response
from api.v1.views import app_endpoints
from api import slashes
from datetime import timedelta
from flask import Flask, jsonify, make_response, abort
from flask_cors import CORS
from models import storage
from models.engine.authentication import authenticate, identity
from os import getenv
from uuid import uuid4

from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt import JWT


'''
app
'''
app = Flask(__name__)
__secret_key = getenv('API_SECRET_KEY')

if not __secret_key:
    raise Exception('API_SECRET_KEY missing')
app.secret_key = __secret_key
CORS(app, resources={r'/*': {'origins': '*'}})
app.debug = True


'''
api
'''
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {
    'title': 'Quimbayas Restful API',
    'uiversion': 1
}
SWAGGER_URL = '/apidocs'
API_URL = '/static/v1.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Quimbayas Restful API'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(app_endpoints)


'''
JWT
'''
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=30)
jwt = JWT(app, authenticate, identity)


'''
error handler
'''


@app.errorhandler(404)
def not_found(e):
    ''' 404 Error
    ---
    response:
      404:
        description: a endpoint was not found
    '''

    return custom_response({'error': 404, 'message': 'not a valid endpoint'})


if __name__ == "__main__":
    ''' Entry point for API '''
    host = getenv('QUIMBAYAS_API_HOST', default='0.0.0.0')
    port = getenv('QUIMBAYAS_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
