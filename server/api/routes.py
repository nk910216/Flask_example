from flask import Blueprint
from flask_restplus import Api

api_bp = Blueprint('version_0', __name__)
api = Api(api_bp)

