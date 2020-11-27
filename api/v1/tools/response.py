#!/usr/bin/env python3
from flask import make_response, jsonify


def custom_response(data, code=None):
    ''' make a api response '''
    if type(data) is not dict:
        raise TypeError('data must be a dict')
    if data.get('error'):
        response = make_response(
            jsonify({'error': data.get('message')}),
            data.get('error')
        )
    else:
        response = make_response(
            jsonify(data),
            code if code else 200
        )

    response.headers['Content-Type'] = 'application/json'

    return response
