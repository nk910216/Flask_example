import base64
from io import BytesIO

from flask import json
from PIL import Image

from server.auth import User
from server.picture import Picture
from server.extensions import db

from .base import BaseTest

def get_test_image_base64():
    img = Image.open('server/tests/img_300.jpg')
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

class PictureApiTest(BaseTest):

    TEST_USER_NAME = 'test'
    TEST_USER_PASSWORD = 'test123'

    picture_base64_str = get_test_image_base64()

    def tearDown(self):
        """ Clean up the picture table for each test
        """
        Picture.query.delete()

    def setUp(self):

        request_header = {
            'Content-Type': 'application/json',
        }

        # reigster user
        user_input = {
            "username": self.TEST_USER_NAME,
            "password": self.TEST_USER_PASSWORD,
        }

        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)

        # login
        response = self.app.post('/api/user/login',
                                 data=request_data,
                                 headers=request_header)
        response_data = json.loads(response.data)
        token = response_data["data"]["token"]
        self.token = token

    def request_header(self):

        request_header = {
            'Content-Type': 'application/json',
            'Authorization': self.token,
        }
        return request_header

    @classmethod
    def encode_data(cls, data):

        return json.dumps(data, ensure_ascii=False).encode('utf8')

    def test_upload_image_with_user_login(self):

        picture_input = {
            "data": bytes.decode(self.picture_base64_str)
        }

        request_header = self.request_header()
        request_data = self.encode_data(picture_input)
        response = self.app.post('/api/picture',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        picture_id = response_data["data"]["id"]

        picture = Picture.query.filter_by(id=picture_id).one()
        self.assertEqual(self.picture_base64_str,
                         picture.data)

    def test_upload_image_without_user_login(self):

        picture_input = {
            "data": bytes.decode(self.picture_base64_str)
        }

        request_header = {
            'Content-Type': 'application/json',
        }
        request_data = self.encode_data(picture_input)
        response = self.app.post('/api/picture',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 403)

    def test_upload_image_with_invalid_token(self):

        picture_input = {
            "data": bytes.decode(self.picture_base64_str)
        }

        request_header = {
            'Content-Type': 'application/json',
            'Authorization': 'abcdefg',
        }
        request_data = self.encode_data(picture_input)
        response = self.app.post('/api/picture',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 401)


    def test_get_picture_without_username(self):

        picture_input = {
            "data": bytes.decode(self.picture_base64_str)
        }

        request_header = self.request_header()
        request_data = self.encode_data(picture_input)
        response = self.app.post('/api/picture',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 201)

        # get data
        response = self.app.get('/api/picture',
                                headers=request_header)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("pictures", response_data["data"])
        self.assertIn("total", response_data["data"])
        self.assertIn("page", response_data["data"])
        self.assertIn("limit", response_data["data"])

        self.assertEqual(1, len(response_data["data"]["pictures"]))
        pic = response_data["data"]["pictures"][0]
        self.assertIn("data", pic)
        self.assertIn("username", pic)
        self.assertIn("id", pic)

        # campare the only one image
        self.assertEqual(picture_input["data"], pic["data"])

    def test_get_picture_with_nonexist_username(self):

        picture_input = {
            "data": bytes.decode(self.picture_base64_str)
        }

        request_header = self.request_header()
        request_data = self.encode_data(picture_input)
        response = self.app.post('/api/picture',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 201)

        # get data
        non_exist_user = "non_exist"
        response = self.app.get('/api/picture?username={}'.format(non_exist_user),
                                headers=request_header)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("pictures", response_data["data"])
        self.assertIn("total", response_data["data"])
        self.assertIn("page", response_data["data"])
        self.assertIn("limit", response_data["data"])

        self.assertEqual(0, len(response_data["data"]["pictures"]))