#!/usr/bin/env python3
''' API index page '''
from api.v1.tools.response import custom_response
from api.v1.views import app_endpoints as endp
from api import slashes
from models import storage


@endp.route('/', methods=['GET'], **slashes)
def status():
    ''' API Status '''
    from api.v1.app import app

    return custom_response({'API': app.config['SWAGGER'], 'status': 'OK'})


@endp.route('/stats', methods=['GET'], **slashes)
def stats():
    ''' API Stats '''

    return custom_response({
        'Total': storage.count(), 'Activities': storage.count('Activities')})
