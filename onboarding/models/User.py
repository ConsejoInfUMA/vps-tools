import secrets

class User:
    PASSWORD_LENGTH = 14

    firstName: str
    lastName: str
    username: str
    password: str
    email: str

    def __init__(self, firstName: str, lastName: str, email: str, username: str = None, password: str = None):
        self.firstName = firstName.lower().title()
        self.lastName = lastName.lower().title()
        self.email = email
        self.username = username if username is not None else self._buildUsername()
        self.password = password if password is not None else self._buildPassword()

    def getFullName(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def _buildUsername(self) -> str:
        return self.email.split('@')[0]

    def _buildPassword(self) -> str:
        return secrets.token_urlsafe(self.PASSWORD_LENGTH)

    def __str__(self) -> str:
        return self.getFullName()
