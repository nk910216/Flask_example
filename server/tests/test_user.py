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

    def test_user_verify_with_correct_password(self):
        """ test the verify_user function for a exist user 
            using correct password
        """
        user = User()
        user.set_data(username=self.TEST_USER_NAME,
                      password=self.TEST_USER_PASSWORD)
        success = user.add_user()
        self.assertTrue(success)
        
        query_user = User.query.first()
        valid = query_user.verify_user(self.TEST_USER_PASSWORD)
        self.assertTrue(valid)

    def test_user_verify_with_wrong_password(self):
        """ test the verify_user function for a exist user 
            using wrong password
        """
        user = User()
        user.set_data(username=self.TEST_USER_NAME,
                      password=self.TEST_USER_PASSWORD)
        success = user.add_user()
        self.assertTrue(success)
        
        wrong_password = self.TEST_USER_PASSWORD + "_"
        query_user = User.query.first()
        valid = query_user.verify_user(wrong_password)
        self.assertFalse(valid)

    def test_user_info_validator_with_correct_input(self):

        correct_input = {
            "username": "rory",
            "password": "123"
        }

        input_data = UserSchema().load(correct_input)
        self.assertTrue(input_data.errors == {})

    def test_user_info_validator_with_wrong_input(self):

        correct_input = {
            "username": "rory",
            "password": "",
        }

        input_data = UserSchema().load(correct_input)
        self.assertTrue(input_data.errors != {})

    def test_user_jwt_token(self):

        user = User()
        user.set_data(username=self.TEST_USER_NAME,
                      password=self.TEST_USER_PASSWORD)
        user.add_user()
        user_id = user.id

        jwt_token = user.encode_auth_token()
        decode_user_id = User.decode_auth_token(jwt_token)
        self.assertEqual(user_id, decode_user_id)
