#!/usr/bin/env python3
''' handles all default RESTful API actions for activities '''
from api.v1.tools.response import custom_response
from api.v1.views import app_endpoints as endp
from api import slashes
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request
from models import storage
from uuid import uuid4


@endp.route('/activities', methods=['GET'], **slashes)
def all_activities():
    '''
    file: documentation/activities/all_activities.yml
    '''
    activities = storage.all('Activities')
    response = custom_response(activities)

    return response


@endp.route('/activities/<string:activity_id>', methods=['GET'], **slashes)
def get_activity(activity_id):
    '''
    file: documentation/activities/get_activity.yml
    '''
    activity = storage.get('Activities', activity_id)
    response = custom_response(activity)

    return response


@endp.route('/activities', methods=['POST'], **slashes)
def post_activity():
    '''
    file: documentation/activities/post_activity.yml
    '''
    doc = {}

    if not request.get_json():
        return custom_response({'error': 400, 'message': 'Not a JSON'})

    data = request.get_json()
    id = data.get('id')
    date = data.get('date')

    if not date:
        return custom_response({
                'error': 400,
                'message': 'The date is missing'
            })

    if id:
        _doc = storage.get('Activities', id)

        print('\n' * 10, '###', _doc, '###')

        if not _doc.get('error'):
            print('into')
            return custom_response({
                'error': 400,
                'message': f'the document <{id}> already exists'
            })
        print('left')
    else:
        id = str(uuid4()).replace('-', '')[0:20]

    data['_class_'] = 'Activities'
    data['id'] = id

    doc.update(data)

    storage.save('Activities', doc)

    return custom_response(
        {'success': f'Document <{id}> created'},
        code=201)


@endp.route('/activities/<string:activity_id>', methods=['PUT'], **slashes)
def put_activity(activity_id):
    '''
    file: documentation/activities/put_activity.yml
    '''
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
def delete_activity(activity_id):
    '''
    file: documentation/activities/delete_activity.yml
    '''

    doc = storage.get('Activities', activity_id)

    if doc.get('error'):
        return custom_response(doc)

    storage.delete('Activities', activity_id)

    return custom_response(
        {'success': f'Document <{activity_id}> deleted'}, code=204)
