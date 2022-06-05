#!/usr/bin/env python3
#
# Small REST API designed to serve a random joke.
#

import logging

from flask import Flask
from flask_json import as_json
from waitress import serve

from config.configservice import ConfigService
from tools.invalid_usage import InvalidUsage
from tools.jsonmngr import JsonMngr

# configure logging
logging.basicConfig()
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

# API init.
api = Flask(__name__)
api.config['JSON_SORT_KEYS'] = False
json_mngr = JsonMngr()


# routing
@as_json
@api.route('/joke/random', methods=['GET'])
def get_joke():
    joke = json_mngr.get_random_joke()
    if joke is None:
        raise InvalidUsage('Nothing jokes here', status_code=500)
    return joke


@as_json
@api.route('/joke/type/<joke_type>', methods=['GET'])
def get_joke_with_type(joke_type):
    joke = json_mngr.get_random_joke_with_type(joke_type)
    if joke is None:
        raise InvalidUsage('Nothing jokes here', status_code=500)
    return joke


@as_json
@api.route('/joke/type/list', methods=['GET'])
def get_categories():
    return json_mngr.get_categories()


# errors
@api.errorhandler(404)
def handle_404(error):
    return {'message': 'Not found', 'status_code': 404}


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = error.to_dict()
    response['status_code'] = error.status_code
    return response


# main
if __name__ == '__main__':
    # load data and start REST API
    json_mngr.load_data()
    serve(api, host='0.0.0.0', port=ConfigService.get('API_PORT'), url_prefix=ConfigService.get('API_BASE_URL'))
