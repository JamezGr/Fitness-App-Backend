import unittest
import pytest

from forms import *
from model import *

email = "unit_test_email@test.com"
username = "unit_test_user"
password = "UNIT_test_password"


class TestLogin(unittest.TestCase):
    def setUp(self):

        print(self._testMethodName)

        self.user = User(email=email, user=username, password=password, confirm_password= password)
        RegisterForm(self.user).create_user()

    def tearDown(self):
         ManageForm(self.user).delete_user()


    # Test with Valid Username + Valid Password
    def test_valid_username(self):        
        self.assertTrue(LoginForm(self.user).check_user_credentials())


    # Test with Valid Username + Invalid Password
    def test_invalid_password(self):
        test_user = User(email=email, user=username, password="password", confirm_password= None)

        if LoginForm(test_user).check_user_exists() is True:
            self.assertFalse(LoginForm(test_user).check_user_credentials(), msg="Password is Valid")
        
        else:
            raise Exception("Username Not Found")

    

# def test_invalid_username(self):
# Test with Invalid Username

# def test_invalid_username(self):
# Test with Invalid Username

# def test_empty_login(self):
# Test with Empty Username + Empty Password


if __name__ == '__main__':
    unittest.main()
