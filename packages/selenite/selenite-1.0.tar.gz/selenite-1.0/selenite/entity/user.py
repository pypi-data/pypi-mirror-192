from typing import Tuple


class User(object):
    """
    User 类代表具有用户名、密码和角色的用户帐户。
    """

    def __init__(self, username: str, password: str, role: str = None):
        """
        使用指定的用户名、密码和角色初始化 User 对象。

        :param username: 用户的用户名。
        :param password: 用户的密码。
        :param role: 用户的角色。
        """
        self._username = username
        self._password = password
        self._role = role

    @property
    def account(self) -> Tuple[str, str]:
        """
        返回一个包含此用户的用户名和密码的元组。
        """
        return self._username, self._password

    @property
    def username(self) -> str:
        """
        返回用户的用户名。
        """
        return self._username

    @property
    def password(self) -> str:
        """
        返回用户的密码。
        """
        return self._password

    def __repr__(self) -> str:
        """
        返回此用户角色的字符串表示形式。
        """
        return self._role
