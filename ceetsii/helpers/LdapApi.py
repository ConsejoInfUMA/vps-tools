import subprocess
from ceetsii.models import User
from requests import Session

class LdapApi:
    s = Session()
    base_url: str
    token: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

        # Connection
        self.s.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def getUsers(self)-> list[User]:
        res = self._req({
            "operationName": "ListUsersQuery",
            "query": """
            query ListUsersQuery($filters: RequestFilter) {
                users(filters: $filters) {
                    id
                    email
                    displayName
                    firstName
                    lastName
                    creationDate
                }
            }
            query ListUserNames($filters: RequestFilter) {
                users(filters: $filters) {
                    id
                    displayName
                }
            }
            """,
            "variables": {
                "filters": None
            }
        })

        users = []
        apiUsers = res["data"]["users"]

        for user in apiUsers:
            users.append(User(
                firstName=user["firstName"],
                lastName=user["lastName"],
                email=user["email"],
                identifier=user["id"],
                displayName=user["displayName"],
                password=''
            ))

        return users

    def addUser(self, user: User) -> bool:
        try:
            self._req({
                "operationName": "CreateUser",
                "query": """
                mutation CreateUser($user: CreateUserInput!) {
                    createUser(user: $user) {
                        id
                        creationDate
                    }
                }
                """,
                "variables": {
                    "user": {
                        "attributes": [
                            {
                                "name": "display_name",
                                "value": [user.displayName]
                            },
                            {
                                "name": "first_name",
                                "value": [user.firstName]
                            },
                            {
                                "name": "last_name",
                                "value": [user.lastName]
                            },
                            {
                                "name": "mail",
                                "value": [user.email]
                            }
                        ],
                        "avatar": None,
                        "displayName": None,
                        "email": None,
                        "firstName": None,
                        "id": user.identifier,
                        "lastName": None
                    }
                }
            })

            # Change password
            cmd = subprocess.run([
                # Producción
                "lldap_set_password",
                # Desarrollo
                #"docker", "compose", "exec", "lldap", "/app/lldap_set_password",
                "--base-url", self.base_url,
                "--token", self.token,
                "--username", user.identifier,
                "--password", user.password
            ])

            return cmd.returncode == 0
        except:
            return False

    def addUserToGroup(self, user: User, group_id: int) -> bool:
        try:
            res = self._req({
                "operationName": "AddUserToGroup",
                "query": """
                mutation AddUserToGroup($user: String!, $group: Int!) {
                    addUserToGroup(userId: $user, groupId: $group) {
                        ok
                    }
                }
                """,
                "variables": {
                    "group": group_id,
                    "user": user.identifier
                }
            })

            return res["data"]["addUserToGroup"]["ok"]
        except:
            return False

    def removeUser(self, user: User) -> bool:
        try:
            res = self._req({
                "operationName": "DeleteUserQuery",
                "query": """
                mutation DeleteUserQuery($user: String!) {
                    deleteUser(userId: $user) {
                        ok
                    }
                }
                """,
                "variables": {
                    "user": user.identifier
                }
            })

            return res["data"]["deleteUser"]["ok"]
        except:
            return False

    def _req(self, body: dict)-> dict:
        res = self.s.post(f"{self.base_url}/api/graphql", json=body)
        if not res.ok:
            raise Exception("Graphql error")

        return res.json()
