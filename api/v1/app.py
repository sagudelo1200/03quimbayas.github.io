#!/usr/bin/env python3
''' RESTful API '''
from api.v1.views import app_endpoints
from models import storage
from flask import Flask, jsonify, make_response, abort
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from os import getenv
from api import slashes
from api.v1.tools.response import custom_response

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {
    'title': 'Quimbayas Restful API',
    'uiversion': 1
}
app.register_blueprint(app_endpoints)
CORS(app, resources={r'/*': {'origins': '*'}})
Swagger(app)


@app.errorhandler(404)
def not_found(e):
    ''' 404 Error
    ---
    response:
      404:
        description: a endpoint was not found
    '''

    return custom_response({'error': 404, 'message': 'not a valid endpoint'})


@app.route('/', methods=['GET'], **slashes)
def status():
    ''' API Status '''

    return custom_response({'API': app.config['SWAGGER'], 'status': 'OK'})


@app.route('/stats', methods=['GET'], **slashes)
def stats():
    ''' API Stats '''

    return custom_response({
        'Total': storage.count(), 'Activities': storage.count('Activities')})


if __name__ == "__main__":
    ''' Entry point for API '''
    host = getenv('QUIMBAYAS_API_HOST', default='0.0.0.0')
    port = getenv('QUIMBAYAS_API_PORT', default=5000)
    app.run(host=host, port=port, debug=True, threaded=True)
