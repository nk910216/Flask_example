import os

class Config(object):
    """ Read the env setting from the env file into the config object
    """
    DB_URI = os.getenv('DB_URI', None)
    SECRET_KEY = os.getenv('SECRET_KEY', '')


class RouteConfig(object):
    API_URI_PREFIX = '/api'