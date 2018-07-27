from flask import request
from flask_restplus import Resource

from server.exceptions import (InvalidPostContent,
                               InvalidPictureFormat,
                               UploadPictureFail)
from server.auth import login_required, User
from server.extensions import db
from server.responses import APIResponse


from .model import Picture
from .utils import PicturePostSchema, simple_check_isBase64

class PicturePostHandler(Resource):

    @login_required
    def get(self, user):

        page = request.args.get('page', '1')
        limit = request.args.get('limit', '20')
        username = request.args.get('username', None)

        try:
            page = int(page)
            limit = int(limit)
        except Exception:
            raise InvalidArgs

        # join the picture with user
        query = db.session.query(User, Picture).join(Picture, User.id==Picture.author_id)

        if username is not None:
            query = query.filter(User.username == username)
        # sort by id descending
        query = query.order_by(Picture.id.desc())

        outputs = query.paginate(page=page, per_page=limit)
        total = outputs.total

        # process the output
        pic_list = []
        for item in outputs.items:
            user = item[0]
            picture = item[1]

            pic = {
                "username": user.username,
                "data": str(picture.data, encoding = "utf-8"),
                "id": picture.id,
            }
            pic_list.append(pic)

        resp = {
            "pictures": pic_list,
            "page": page,
            "limit": limit,
            "total": total
        }

        ret = APIResponse(resp)
        return ret.get_json(), 200

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

