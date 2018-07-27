from server.auth import User

from .base import BaseTest

class UserApiTest(BaseTest):

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

