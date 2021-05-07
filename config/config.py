import base64
import os

# init dict.
cfg = {}

## get env. variables
cfg['API_BASE_URL'] = os.getenv('API_BASE_URL')
cfg['API_PORT'] = os.getenv('API_PORT')
cfg['JSON_FILE_PATH'] = os.getenv('JSON_FILE_PATH')

## default values if missing
if cfg['API_BASE_URL'] == None:
    cfg['API_BASE_URL'] = '/'
if cfg['API_PORT'] == None:
    cfg['API_PORT'] = 5000

## check all runtime parameters
def check_runtime_cfg():
    unset_params = []
    # check every config parameters
    for k, v in cfg.items():
        if v == None:
            unset_params.append(k)
    # if at least one parameter is not set, display and exit
    if unset_params != []:
        print('missing runtime parameter(s) :')
        for param in unset_params:
            print(' - %s' % param)
        print('to fix this : set missing runtime parameter(s), then restart this app')
        exit(1)
