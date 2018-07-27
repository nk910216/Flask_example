from flask import Blueprint
from flask_restplus import Api

from server import auth

api_bp = Blueprint('version_0', __name__)
api = Api(api_bp)

# auth
api.add_resource(auth.RegisterHandler, '/user/register')
api.add_resource(auth.LoginHandler, '/user/login')