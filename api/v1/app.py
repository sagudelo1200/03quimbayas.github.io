#!/usr/bin/env python3
''' RESTful API '''
from api.v1.views import app_endpoints
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_endpoints)
CORS(app, resources={r'/*': {'origins': '*'}})

slashes = {'strict_slashes': True}


@app.errorhandler(404)
def not_found(e):
    ''' 404 Error
    ---
    response:
      404:
        description: a resource was not found
    '''
    response = make_response(
        jsonify({'error': "Resource not found!"}),
        404
    )

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/status', methods=['GET'], **slashes)
def status():
    ''' API Status '''
    response = make_response(
        jsonify({'status': 'OK'}),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    ''' Entry point for API '''
    host = getenv('QUIMBAYAS_API_HOST', default='0.0.0.0')
    port = getenv('QUIMBAYAS_API_PORT', default=7000)
    app.run(host=host, port=port, debug=True, threaded=True)
