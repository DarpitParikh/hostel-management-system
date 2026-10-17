"""Login checking."""


class Authenticator:
    """Only checks username and password. Users are given from outside."""

    def __init__(self, users):
        self.users = users

    def login(self, username, password):
        return username in self.users and self.users[username] == password
