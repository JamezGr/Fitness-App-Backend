class User(object):
    def __init__(self, email=None, user=None, password=None, confirm_password=None):
        self.email = email
        self.user = user
        self.password = password
        self.confirm_password = confirm_password
