from flask import request
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound

from server.exceptions import (InvalidPostContent,
                               UserAlreadyExist,
                               UsernameNotExist,
                               UserWrongPassword,
                               InvalidUsername,
                               InvalidPassword)

from server.responses import APIResponse

from .model import User
from .utils import UserSchema, valid_auth_string


class RegisterHandler(Resource):

    def post(self):

        data = request.get_json(silent=True)
        if not data:
            raise InvalidPostContent

        input_data = UserSchema().load(data)
        if input_data.errors:
            raise InvalidPostContent

        args = input_data.data
        username = args["username"]
        password = args["password"]

        if not valid_auth_string(username):
            raise InvalidUsername
        if not valid_auth_string(password):
            raise InvalidPassword

        user = User()
        user.set_data(username=username,
                      password=password)
        success = user.add_user()
        if not success:
            raise UserAlreadyExist

        ret = APIResponse({'username': username})
        return ret.get_json(), 200


class LoginHandler(Resource):

    def post(self):

        data = request.get_json(silent=True)
        if not data:
            raise InvalidPostContent

        input_data = UserSchema().load(data)
        if input_data.errors:
            raise InvalidPostContent

        args = input_data.data
        username = args["username"]
        password = args["password"]

        try:
            user = User.query.filter_by(username=username).one()
        except NoResultFound:
            raise UsernameNotExist

        if not user.verify_user(password):
            raise UserWrongPassword

        jwt_token = str(user.encode_auth_token())
        ret = APIResponse({'token': jwt_token})
        return ret.get_json(), 200
