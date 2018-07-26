from flask import Flask

from .api.routes import api_bp, api
from .config import Config, RouteConfig
from .responses import ErrorResponse

def init_app():
    """ Init the whole application
    """

    app = Flask(__name__)

    # initialize the config
    init_config(app)

    # initialize the route
    init_route(app)

    # initialize error handler
    init_errorhandler(api)

    return app


def init_config(app):
    """ Initialize the app setting using config object
    """
    app.config.from_object(Config)


def init_route(app):
    """ Initialize tha routing for the app
    """
    api_uri_prefix = RouteConfig.API_URI_PREFIX

    app.register_blueprint(api_bp, url_prefix=api_uri_prefix)


def init_errorhandler(api):
    """ Initialize the error handle function for flask_restplus
    """
    @api.errorhandler
    def internal_error_handler(error):
        ret = ErrorResponse(code=1, message="SOMETHING WRONG WITH THE SERVER")
        return ret.get_json(), 500
