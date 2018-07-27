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

    def test_register_api(self):
        """ test register api with valid input
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
