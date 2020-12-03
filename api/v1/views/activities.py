#!/usr/bin/env python3
''' handles all default RESTful API actions for activities '''
from api.v1.tools.response import custom_response
from api.v1.views import app_endpoints as endp
from api import slashes
from flask_jwt import jwt_required
from flask import abort, jsonify, make_response, request
from models import storage
from uuid import uuid4
from models.activity import Activity
import models


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

    if activity:
        activity['__class__'] = activity.get('_class_') or activity.get(
            '__class__')

        obj = models.from_dict(activity)

        response = custom_response(obj.to_dict())
    else:
        response = custom_response({
            'error': 404,
            'message': f"The document <{activity_id}> does not exists"})
    return response


@endp.route('/activities', methods=['POST'], **slashes)
@jwt_required()
def post_activity():
    '''
    file: documentation/activities/post_activity.yml
    '''
    doc = {}

    if not request.get_json():
        return custom_response({'error': 400, 'message': 'Not a JSON'})

    data = request.get_json()
    id = data.get('id') or str(uuid4()).replace('-', '')[:20]

    if storage.exists('Activities', id):
        return custom_response({
            'error': 400,
            'message': f'the document <{id}> already exists'
        })

    data['id'] = id

    doc.update(data)

    obj = Activity(**doc)
    obj.save()

    return custom_response(
        {'success': f'Document <{id}> created'},
        code=201)


@endp.route('/activities/<string:activity_id>', methods=['PUT'], **slashes)
@jwt_required()
def put_activity(activity_id):
    '''
    file: documentation/activities/put_activity.yml
    '''
    doc = {}

    if not request.get_json():
        return custom_response({'error': 400, 'message': 'Not a JSON'})

    activity = storage.get('Activities', activity_id)

    if not activity:
        return custom_response({
                'error': 404,
                'message': f'the document <{activity_id}> does not exists'
            })

    data = request.get_json()
    data['id'] = activity_id

    doc.update(data)

    obj = Activity(**doc)
    obj.save()

    return custom_response({'success': f'Document <{activity_id}> updated'})


@endp.route('/activities/<string:activity_id>', methods=['DELETE'], **slashes)
@jwt_required()
def delete_activity(activity_id):
    '''
    file: documentation/activities/delete_activity.yml
    '''

    if storage.exists('Activities', activity_id):
        storage.delete('Activities', activity_id)
        return custom_response({}, code=204)
    else:
        return custom_response({
                'error': 404,
                'message': f'the document <{activity_id}> does not exists'
            })
