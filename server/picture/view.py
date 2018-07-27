from flask import request
from flask_restplus import Resource

from server.exceptions import (InvalidPostContent,
                               InvalidPictureFormat,
                               UploadPictureFail)
from server.auth import login_required
from server.responses import APIResponse

from .model import Picture
from .utils import PicturePostSchema, simple_check_isBase64

class PicturePostHandler(Resource):

    @login_required
    def post(self, user):

        data = request.get_json(silent=True)
        if not data:
            raise InvalidPostContent

        input_data = PicturePostSchema().load(data)
        if input_data.errors:
            raise InvalidPostContent

        args = input_data.data
        picture_str = args["data"]  # str

        # simply verify the base64 image
        picture_byte, is_base64 = simple_check_isBase64(picture_str)
        if not is_base64:
            raise InvalidPictureFormat

        picture = Picture()
        picture.set_data(data=picture_byte,
                         author_id=user.id)
        success = picture.add_picture()

        if not success:
            raise UploadPictureFail

        ret = APIResponse({'id': picture.id})
        return ret.get_json(), 201

