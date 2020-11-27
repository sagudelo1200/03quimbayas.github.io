#!/usr/bin/env python3
''' handles all default RESTful API actions for activities '''
from api import slashes
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from api.v1.views import app_endpoints as endp
from api.v1.tools.response import custom_response
from uuid import uuid4

from time import sleep


@endp.route('/activities', methods=['GET'], **slashes)
@swag_from('documentation/activities/all_activities.yml')
def all_activities():
    ''' Retrieves a list of all activities '''
    activities = storage.all('Activities')
    response = custom_response(activities)

    return response


@endp.route('/activities/<string:activity_id>', methods=['GET'], **slashes)
@swag_from('documentation/activities/get_activity.yml')
def get_activity(activity_id):
    ''' Retrieves a activity with the especified id '''
    activity = storage.get('Activities', activity_id)
    response = custom_response(activity)

    return response


@endp.route('/activities/<string:activity_id>', methods=['POST'], **slashes)
@swag_from('documentation/activities/post_activity.yml')
def post_activity(activity_id):
    ''' Create an activity '''
    doc = {}

    if not request.get_json():
        return custom_response({'error': 400, 'message': 'Not a JSON'})

    _doc = storage.get('Activities', activity_id)

    if not _doc or not _doc.get('error'):
        return custom_response({
            'error': 400,
            'message': f'the document <{activity_id}> already exists'
        })

    data = request.get_json()
    if activity_id == 'create':
        activity_id = str(uuid4()).replace('-', '')[0:20]

    data['_class_'] = 'Activities'
    data['id'] = activity_id

    doc.update(data)

    storage.save('Activities', doc)

    return custom_response(
        {'success': f'Document <{activity_id}> created'},
        code=201)


@endp.route('/activities/<string:activity_id>', methods=['PUT'], **slashes)
@swag_from('documentation/activities/put_activity.yml')
def put_activity(activity_id):
    ''' Update an activity '''
    doc = {}

    if not request.get_json():
        return custom_response({'error': 400, 'message': 'Not a JSON'})

    activity = storage.get('Activities', activity_id)

    if activity.get('error'):
        return custom_response(activity)

    data = request.get_json()

    data['id'] = activity_id

    doc.update(data)

    storage.save('Activities', doc, merge=True)

    return custom_response({'success': f'Document <{activity_id}> updated'})


@endp.route('/activities/<string:activity_id>', methods=['DELETE'], **slashes)
@swag_from('documentation/activities/delete_activity.yml')
def delete_activity(activity_id):
    ''' Delete an activity '''

    doc = storage.get('Activities', activity_id)

    if doc.get('error'):
        return custom_response(doc)

    storage.delete('Activities', activity_id)

    return custom_response({'success': f'Document <{activity_id}> deleted'})
