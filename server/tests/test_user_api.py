from flask import json

from server.auth import User
from server.auth.utils import UserSchema

from .base import BaseTest

class UserTest(BaseTest):

    TEST_USER_NAME = 'test'
    TEST_USER_PASSWORD = 'test123'

    def tearDown(self):
        """ Clean up the user table for each test
        """
        User.query.delete()

    @classmethod
    def request_header(cls):

        request_header = {
            'Content-Type': 'application/json'
        }
        return request_header

    @classmethod
    def encode_data(cls, data):

        return json.dumps(data, ensure_ascii=False).encode('utf8')

    def add_user(self):
        user_input = {
            "username": self.TEST_USER_NAME,
            "password": self.TEST_USER_PASSWORD,
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 200)

    def test_register_api(self):
        """ test register api with valid input
        """
        self.add_user()

    def test_register_api_with_same_username(self):
        """ test register api with already exist user
        """

        user_input = {
            "username": self.TEST_USER_NAME,
            "password": self.TEST_USER_PASSWORD,
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 409)

    def test_register_api_with_empty_password(self):
        """ test register api with invalid content
        """

        user_input = {
            "username": self.TEST_USER_NAME,
            "password": "",
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 400)

    def test_register_api_with_tooshort_username(self):
        """ test register api with too short username
        """

        user_input = {
            "username": "a",
            "password": self.TEST_USER_NAME,
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 400)

    def test_register_api_with_tooshort_password(self):
        """ test register api with too short password
        """

        user_input = {
            "username": self.TEST_USER_NAME,
            "password": "b",
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/register',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 400)

    def test_user_login_api_with_corrent_data(self):
        """ test register api with invalid content
        """
        self.add_user()

        user_input = {
            "username": self.TEST_USER_NAME,
            "password": self.TEST_USER_PASSWORD,
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/login',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("token", response_data["data"])

    def test_user_login_api_with_non_exist_user(self):
        """ test register api with non exist user
        """
        self.add_user()

        user_input = {
            "username": self.TEST_USER_NAME + "_",
            "password": self.TEST_USER_PASSWORD,
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/login',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 404)

    def test_user_login_api_with_wrong_password(self):
        """ test register api with wrong password
        """
        self.add_user()

        user_input = {
            "username": self.TEST_USER_NAME,
            "password": self.TEST_USER_PASSWORD + "_",
        }

        request_header = self.request_header()
        request_data = self.encode_data(user_input)
        response = self.app.post('/api/user/login',
                                 data=request_data,
                                 headers=request_header)
        self.assertEqual(response.status_code, 401)
