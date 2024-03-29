import unittest
import pytest

from api.forms.forms import ManageForm
from api.forms.register_user import RegisterForm
from api.forms.login_user import LoginForm
from api.models.user import User

email = "unit_test_email@test.com"
username = "unit_test_user"
password = "UNIT_test_password"


class TestLogin(unittest.TestCase):
    def setUp(self):

        print(self._testMethodName)

        self.user = User(email=email, user=username, password=password, confirm_password=password)
        RegisterForm(self.user).create_username()

    def tearDown(self):
         ManageForm(username).delete_user()

    # Test with Valid Username + Valid Password
    def test_valid_username(self):        
        self.assertTrue(LoginForm(self.user).check_user_credentials())


    # Test with Valid Username + Invalid Password
    def test_invalid_password(self):
        test_user = User(email=email, user=username, password="password", confirm_password= None)

        if LoginForm(test_user).check_username_exists() is True:
            self.assertFalse(LoginForm(test_user).check_user_credentials(), msg="Password is Valid")
        
        else:
            raise Exception("Username Not Found")

    

    # Test with Invalid Username
    def test_invalid_username(self):
        test_user = User(email=email, user="TEST_INVALID_USERNAME", password="TEST_INVALID_PASSWORD", confirm_password= None)
        self.assertFalse(LoginForm(test_user).check_username_exists())


    def test_empty_login(self):
        test_user = User(email=email, user="", password="", confirm_password= None)
        self.assertFalse(LoginForm(test_user).check_username_exists())

if __name__ == '__main__':
    unittest.main()
