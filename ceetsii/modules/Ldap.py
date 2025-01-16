import csv

from os.path import isfile

from requests import Session
from ceetsii.modules.Base import Base
from ceetsii.helpers import Option, User


class Ldap(Base):
    s = Session()

    base_url: str
    options: list

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.options = [
            Option(
                'Listar',
                self.enum
            ),
            Option(
                'Importar',
                self.csv
            )
        ]

        # Connection
        self.s.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def main(self):
        self._pick(self.options, "Elige una acción")

    def enum(self):
        users = self._getUsers()
        self._printUsers(users)

    def csv(self):
        """
        Actualmente el excel tiene la siguiente estructura:
        Columna 1: Nombre
        Columna 2: Apellidos
        Columna 3: Correo electrónico
        """

        csvStr = input("Escribe el path en el que se encuentra el documento:")
        
        if not isfile(csvStr):
            raise Exception("Ese archivo no existe")
        
        excel_users = []
        ldap_users = self._getUsers()

        with open(csvStr) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            next(reader, None)  # Ignoramos el header
            for row in reader:
                # Evitamos incluir usuarios en blanco
                if row[2] != "":
                    excel_users.append(User(
                        firstName=row[0],
                        lastName=row[1],
                        email=row[2],
                        autogen_password=True
                    ))
        
        # Eliminamos duplicados
        filtered_excel_users = list(set(excel_users))

        users_add = [u for u in filtered_excel_users if u not in ldap_users]
        users_ok = [u for u in ldap_users if u in filtered_excel_users]
        users_remove = [u for u in ldap_users if u.identifier != 'admin' and u not in filtered_excel_users]

        # Sort all
        users_add.sort(key=lambda u: u.firstName)
        users_ok.sort(key=lambda u: u.firstName)
        users_remove.sort(key=lambda u: u.firstName)

        print("Añadir:")
        print("-----")
        self._printUsers(users_add)
        print("-----")
        print("No modificar:")
        print("-----")
        self._printUsers(users_ok)
        print("-----")
        print("Eliminar:")
        print("-----")
        self._printUsers(users_remove)
        print("-----")

        
    
    def _getUsers(self)-> list[User]:
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
                autogen_password=False
            ))
        
        return users
    
    def _printUsers(self, users: list[User]):
        for user in users:
            print(f"{user.displayName} ({user.email})")

    def _req(self, body: dict)-> dict:
        res = self.s.post(f"{self.base_url}/api/graphql", json=body)
        if not res.ok:
            raise Exception("Graphql error")
        
        return res.json()
