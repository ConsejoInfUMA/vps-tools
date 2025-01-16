import secrets
from typing import Self

class User:
    firstName: str
    lastName: str
    email: str
    subject: str
    identifier: str
    displayName: str
    password: str

    def __init__(self, firstName: str, lastName: str, email: str, subject: str, identifier: str = None, displayName: str = None, password: str = None):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.subject = subject

        if identifier is None:
            self.identifier = self.email.split('@')[0]
        else:
            self.identifier = identifier

        if displayName is None:
            self.displayName = f"{self.firstName} {self.lastName}"
        else:
            self.displayName = displayName

        if password is None:
            self.password = secrets.token_urlsafe(16)
        else:
            self.password = password

    @staticmethod
    def fromRow(row: list) -> Self:
        return Self(
            firstName=row[0],
            lastName=row[1],
            email=row[2],
            subject=row[3],
            identifier=row[4],
            displayName=row[5],
            password=row[6]
        )

    def toRow(self) -> list:
        return [
            self.firstName,
            self.lastName,
            self.email,
            self.subject,
            self.identifier,
            self.displayName,
            self.password
        ]

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return self.identifier.__hash__()

    def __str__(self) -> str:
        return f"{self.displayName} ({self.email})"
