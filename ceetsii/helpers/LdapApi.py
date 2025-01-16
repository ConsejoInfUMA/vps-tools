from ceetsii.helpers import User
from requests import Session

class LdapApi:
    s = Session()
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url

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

    def _req(self, body: dict)-> dict:
        res = self.s.post(f"{self.base_url}/api/graphql", json=body)
        if not res.ok:
            raise Exception("Graphql error")

        return res.json()
