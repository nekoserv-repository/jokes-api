import os


class ConfigService:
    __cfg = None

    @staticmethod
    def get(value):
        """init configuration if needed, then return item from __cfg"""
        # reload
        ConfigService.__load_env()
        # get config
        return ConfigService.__cfg[value]

    @staticmethod
    def __load_env():
        """get all env. variables and check configuration"""
        ConfigService.__cfg = {'API_BASE_URL': os.getenv('API_BASE_URL'),
                               'API_PORT': os.getenv('API_PORT'),
                               'JSON_FILE_PATH': os.getenv('JSON_FILE_PATH')}
        ConfigService.__set_default_values()
        return ConfigService.__check()

    @staticmethod
    def __check():
        is_valid = True
        # check all environment variables
        for k, v in ConfigService.__cfg.items():
            # display which environment variable is not set
            if v is None:
                print('runtime parameter "%s" is not set' % k)
                is_valid = False
        # exit if not valid
        if not is_valid:
            exit(1)
        return is_valid

    @staticmethod
    def __set_default_values():
        if ConfigService.__cfg['API_BASE_URL'] is None:
            ConfigService.__cfg['API_BASE_URL'] = '/'
        if ConfigService.__cfg['API_PORT'] is None:
            ConfigService.__cfg['API_PORT'] = 5000
