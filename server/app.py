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

    @api.errorhandler(exceptions.UsernameNotExist)
    def user_not_exist(error):
        ret = ErrorResponse(code=4, message="USER NOT EXIST")
        return ret.get_json(), 404

    @api.errorhandler(exceptions.UserWrongPassword)
    def user_wrong_password(error):
        ret = ErrorResponse(code=5, message="USER WRONG PASSWORD")
        return ret.get_json(), 401

    @api.errorhandler(exceptions.InvalidPictureFormat)
    def invalid_picture_format(error):
        ret = ErrorResponse(code=6, message="PICTURE DATA IS NOT BASE64 ENCODE")
        return ret.get_json(), 400

    @api.errorhandler(exceptions.NoAuthToken)
    def no_auth_token(error):
        ret = ErrorResponse(code=7, message="NO AUTH TOKEN IN HEADER")
        return ret.get_json(), 403

    @api.errorhandler(exceptions.JWTExpireTime)
    def jwt_expire(error):
        ret = ErrorResponse(code=8, message="TOKEN EXPIRE TIME")
        return ret.get_json(), 401

    @api.errorhandler(exceptions.InvalidJWTToken)
    def invalid_token(error):
        ret = ErrorResponse(code=9, message="TOKEN INVALID")
        return ret.get_json(), 401

    @api.errorhandler(exceptions.UploadPictureFail)
    def upload_picture_fail(error):
        ret = ErrorResponse(code=10, message="UPLOAD PICTURE FAIL")
        return ret.get_json(), 500