from typing import Tuple


class Account:
    """
    The User class represents a user account with a username, password, and role.
    """

    def __init__(self, username: str, password: str, role: str = None):
        """
        Initializes a User object with the specified username, password, and role.

        :param username: The user's username.
        :param password: The user's password.
        :param role: The user's role.
        """
        self._username = username
        self._password = password
        self._role = role

    @property
    def account(self) -> Tuple[str, str]:
        """
        Returns a tuple containing this user's username and password.
        """
        return self._username, self._password

    @property
    def username(self) -> str:
        """
        Returns the user's username.
        """
        return self._username

    @property
    def password(self) -> str:
        """
        Returns the user's password.
        """
        return self._password

    def __repr__(self) -> str:
        """
        Returns a string representation of this user's role.
        """
        return self._role
