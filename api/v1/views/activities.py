#!/usr/bin/env python3
''' handles all default RESTful API actions for activities '''
from api.v1.views import app_endpoints as endp
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from api import slashes
from collections import storage


@endp.route('/activities', methods=['GET'], **slashes)
@swag_from('documentation/activities/all_activities.yml')
def get_activities():
    ''' Retrieves a list of all activities '''
    activities = storage.all('Activities')
    status = 400 if activities.get('error') else 200

    return make_response(
        jsonify(activities),
        status
    )
