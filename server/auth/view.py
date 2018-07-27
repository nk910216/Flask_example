from flask import request
from flask_restplus import Resource

from server.exceptions import (InvalidPostContent,
                               UserAlreadyExist)
from server.responses import APIResponse

from .model import User
from .utils import UserSchema


class RegisterHandler(Resource):

    def post(self):

        data = request.get_json(silent=True)
        if not data:
            raise InvalidPostContent

        input_data = UserSchema().load(data)
        if input_data.errors:
            raise InvalidPostContent

        args = input_data.data
        user = User()
        user.set_data(username=args["username"],
                      password=args["password"])
        success = user.add_user()
        if not success:
            raise UserAlreadyExist

        ret = APIResponse({'username': args["username"]})
        return ret.get_json(), 200

