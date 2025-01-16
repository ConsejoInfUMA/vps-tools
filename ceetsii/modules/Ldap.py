import csv

from os import remove as removefile
from os.path import isfile

from ceetsii.modules.Base import Base
from ceetsii.helpers import Option, User, LdapApi


class Ldap(Base):
    api: LdapApi
    out_dir = "out"
    options: list

    def __init__(self, base_url: str, token: str, out_dir: str):
        self.base_url = base_url
        self.out_dir = out_dir
        self.options = [
            Option(
                'Listar',
                self.enum
            ),
            Option(
                'Importar',
                self.csv
            ),
            Option(
                'Aplicar CSV generado',
                self.commit
            )
        ]

        self.api = LdapApi(base_url, token)

    def main(self):
        self._pick(self.options, "Elige una acción")

    def enum(self):
        users = self.api.getUsers()
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
        ldap_users = self.api.getUsers()

        with open(csvStr) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            next(reader, None)  # Ignoramos el header
            for row in reader:
                # Evitamos incluir usuarios en blanco
                if row[2] != "":
                    excel_users.append(User(
                        firstName=row[0],
                        lastName=row[1],
                        email=row[2]
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

        # Generamos los csvs
        self._writeUsersCsv(users_add, 'add.csv')
        self._writeUsersCsv(users_ok, 'ok.csv')
        self._writeUsersCsv(users_remove, 'remove.csv')

        print("Se han generado los csvs con los cambios a hacer al servidor LDAP")

    def commit(self):
        pass

    def _printUsers(self, users: list[User]):
        for user in users:
            print(f"{user.displayName} ({user.email})")

    def _writeUsersCsv(self, users: list[User], filename: str):
        path = f"{self.out_dir}/{filename}"
        if isfile(path):
            removefile(path)

        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Nombre", "Apellidos", "Email", "Nombre de usuario", "Nombre completo", "Contraseña"])
            for user in users:
                writer.writerow(user.toRow())
