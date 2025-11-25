import csv
import json
from typing import List
from onboarding.models.User import User

class Csv:
    users = []

    def __init__(self, path: str, fistNameKey: str, lastNameKey: str, emailKey: str):
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                firstName = row[fistNameKey].strip()
                lastName = row[lastNameKey].strip()
                email = row[emailKey].strip()

                if email is not None and email != '':
                    user = User(firstName, lastName, email)
                    self.users.append(user)

    def getUserByEmail(self, email: str) -> User:
        users = list(filter(lambda user: user.email == email, self.users))
        return users[0] if len(users) > 0 else None
