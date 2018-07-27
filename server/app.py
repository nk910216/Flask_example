from flask import Flask, current_app

from .api.routes import api_bp, api
from .config import Config, RouteConfig
from .extensions import db
from . import exceptions
from .responses import ErrorResponse

def init_app():
    """ Init the whole application
    """

    app = Flask(__name__)

    # initialize the config
    init_config(app)

    # initialize the route
    init_route(app)

    # initialize the database
    init_db(app)

    # initialize error handler
    init_errorhandler(api)

    return app


def init_config(app):
    """ Initialize the app setting using config object
    """
    app.config.from_object(Config)


def init_db(app):
    """ Initialize the database setting
    """

    db_uri = Config.DB_URI
    if not db_uri:
        raise Exception("No DB_URI in env file!")

    app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    with app.app_context():
        db.init_app(app)

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
        current_app.logger.error(error)
        ret = ErrorResponse(code=1, message="SOMETHING WRONG WITH THE SERVER")
        return ret.get_json(), 500

    @api.errorhandler(exceptions.InvalidPostContent)
    def invalid_post_content_handler(error):
        ret = ErrorResponse(code=2, message="INVALID POST CONTENT")
        return ret.get_json(), 400

    @api.errorhandler(exceptions.UserAlreadyExist)
    def user_already_exist_handler(error):
        ret = ErrorResponse(code=3, message="USER ALREADY EXIST")
        return ret.get_json(), 409
