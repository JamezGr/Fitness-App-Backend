import unittest
import pytest

from api.forms.forms import *
from api.models.user import User

"""Valid Credentials For Testing """
email = "unit.test@unittest.com"
username = "unit_test_user"
password = "UNIT_test_password12"

class TestRegister(unittest.TestCase):
    """Should Accept Valid Email """
    def test_valid_email(self):
        test_user = User(email=email, user=None, password=None, confirm_password=None)
        
        self.assertTrue(RegisterForm(test_user).check_email_valid())

    """Should Accept Valid Username """
    def test_valid_username(self):
        test_user = User(email=None, user=username, password=None, confirm_password=None)

        self.assertTrue(RegisterForm(test_user).check_username_valid())

    """Should Accept Valid Password """
    def test_valid_password(self):
        test_user = User(email=None, user=None, password=password, confirm_password=password)

        self.assertTrue(RegisterForm(test_user).check_password_valid())
    
    """Should Register New Account with Valid Credentials """
    def test_user_register(self):
        test_user = User(email=email, user=username, password=password, confirm_password=password)

        RegisterForm(test_user).create_username()

        self.assertTrue(RegisterForm(test_user).check_username_exists())
        ManageForm(test_user).delete_user()


    # should not accept invalid email format
    # should not accept username with illegal characters '&=()<>+,'
    # should not accept username less than min length (3 characters)
    # should not accept username with more than max characters (30 characters)

    # should not accept passwords less than min length (8 characters)
    # should not accept passwords more than max length (32 characters)

    # should not accept passwords which do not meet at least 3 requirements see api/forms/forms.py - RegisterForm

if __name__ == '__main__':
    unittest.main()