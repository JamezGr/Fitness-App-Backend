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
    def setUp(self):
        print(self._testMethodName)

    def tearDown(self):
        print("\n")

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
        ManageForm(username).delete_user()
    
    """Should Not Accept Invalid Email Format """
    def test_invalid_email_format(self):
        test_user = User(email="unittestgmail.com", user=username, password=password, confirm_password=password)

        self.assertFalse(RegisterForm(test_user).check_email_valid())

    """Should Not Accept Empty Username """
    def test_empty_username(self):
        test_user = User(email=email, user="", password=password, confirm_password=password)

        self.assertFalse(RegisterForm(test_user).check_username_valid())

    """Should Not Accept Username with Illegal Characters """
    def test_username_for_illegal_characters(self):
        test_user = User(email=email, user="username&()=", password=password, confirm_password=password)

        self.assertFalse(RegisterForm(test_user).check_username_valid())

    """Should Not Accept Username Less than Minimum Length (3 Characters) """
    def test_username_less_than_min_length(self):
        test_user = User(email=email, user="us", password=password, confirm_password=password)

        self.assertFalse(RegisterForm(test_user).check_username_valid())

    """Should Not Accept Username More than Maximum Length (30 Characters) """
    def test_username_more_than_max_length(self):
        test_user = User(email=email, user="usernameusernameusernameusername", password=password, confirm_password=password)

        self.assertFalse(RegisterForm(test_user).check_username_valid())

    """Should Not Accept Passwords which do not meet at least 3 Requirements """
    def test_invalid_password(self):
        test_user = User(email=email, user=username, password="password", confirm_password="password")

        self.assertFalse(RegisterForm(test_user).check_password_valid())

    """Should Not Accept Empty Password """
    def test_empty_password(self):
        test_user = User(email=email, user=username, password="", confirm_password="")

        self.assertFalse(RegisterForm(test_user).check_password_valid())

if __name__ == '__main__':
    unittest.main()