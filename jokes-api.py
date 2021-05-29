#!/usr/bin/env python3
#
# Small REST API designed to serve a random joke.
#

from config.config import check_runtime_cfg
from config.config import cfg
from tools.json_mngr import JSON_Mngr
from tools.invalid_usage import InvalidUsage

from waitress import serve
from flask import Flask
from flask_json import as_json

import logging
import json


## configure logging
logging.basicConfig()
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

## API init.
api = Flask(__name__)
api.config['JSON_SORT_KEYS'] = False
data_mngr = JSON_Mngr()


## routing
@as_json
@api.route('/joke/random', methods=['GET'])
def get_joke():
    joke = data_mngr.get_random_joke()
    if joke == None:
        raise InvalidUsage('Nothing jokes here', status_code=500)
    return joke

@as_json
@api.route('/joke/type/<joke_type>', methods=['GET'])
def get_joke_with_type(joke_type):
    joke = data_mngr.get_random_joke_with_type(joke_type)
    if joke == None:
        raise InvalidUsage('Nothing jokes here', status_code=500)
    return joke

@as_json
@api.route('/joke/type/list', methods=['GET'])
def get_categories():
    return data_mngr.get_categories()

## errors
@api.errorhandler(404)
def handle_404(error):
    return { 'message':'Not found', 'status_code':404}

@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = error.to_dict()
    response['status_code'] = error.status_code
    return response

## main
if __name__ == '__main__':
    # check runtime configuration, load data and start REST API
    check_runtime_cfg()
    data_mngr.load_data()
    serve(api, host='0.0.0.0', port=cfg['API_PORT'], url_prefix=cfg['API_BASE_URL'])