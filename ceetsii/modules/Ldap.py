import csv
from os import remove as removefile
from os.path import isfile

from ceetsii.modules.Base import Base
from ceetsii.helpers import LdapApi, Mail
from ceetsii.models import Option, User

class Ldap(Base):
    api: LdapApi
    mail: Mail
    base_url: str
    input_path: str
    out_dir = "out"
    group_id: int
    options: list

    def __init__(self, base_url: str, input_path: str, token: str, out_dir: str, group_id: int, mail_host: str, mail_port: int, mail_user: str, mail_pass: str):
        self.base_url = base_url
        self.input_path = input_path
        self.out_dir = out_dir
        self.group_id = group_id
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
            ),
            Option(
                'Enviar correos de bienvenida',
                self.welcome
            )
        ]

        self.api = LdapApi(base_url, token)
        self.mail = Mail(mail_host, mail_port, mail_user, mail_pass, base_url)

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
        Columna 10: Asignatura que representa
        """

        if not isfile(self.input_path):
            raise Exception("Ese archivo no existe")

        excel_users = []
        ldap_users = self.api.getUsers()

        with open(self.input_path) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            next(reader, None)  # Ignoramos el header
            for row in reader:
                # Evitamos incluir usuarios en blanco
                if row[2] != "":
                    excel_users.append(User(
                        firstName=row[0],
                        lastName=row[1],
                        email=row[2],
                        subject=row[9]
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
        users_add = self._readCommitCsv('add.csv')
        users_remove = self._readCommitCsv('remove.csv')

        self._commitAdd(users_add)
        self._commitRemove(users_remove)

    def welcome(self):
        users_add = self._readCommitCsv('add.csv')

        self.mail.sendWelcome(users_add)

    def _commitAdd(self, users: list[User]):
        for user in users:
            # Add user
            ok = self.api.addUser(user)
            if not ok:
                print(f"{user} Error al agregar, deteniendo proceso")
                break

            # Add to group
            ok = self.api.addUserToGroup(user, self.group_id)
            if not ok:
                print(f"{user} Error al agregar a grupo, deteniendo proceso")
                break

            print(f"{user} agregado con éxito")

    def _commitRemove(self, users: list[User]):
        for user in users:
            ok = self.api.removeUser(user)
            if not ok:
                print(f"{user} Error al eliminar, deteniendo progreso")
                break

            print(f"{user} eliminado con éxito")

    def _printUsers(self, users: list[User]):
        for user in users:
            print(f"{user.displayName} ({user.email})")

    def _readCommitCsv(self, filename: str) -> list[User]:
        path = f"{self.out_dir}/{filename}"
        if not isfile(path):
            raise Exception(f"{path} no existe")

        users = []
        with open(path) as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            next(reader, None)  # Ignoramos el header
            for row in reader:
                users.append(User(
                    firstName=row[0],
                    lastName=row[1],
                    email=row[2],
                    subject=row[3],
                    identifier=row[4],
                    displayName=row[5],
                    password=row[6]
                ))

        return users

    def _writeUsersCsv(self, users: list[User], filename: str):
        path = f"{self.out_dir}/{filename}"
        if isfile(path):
            removefile(path)

        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Nombre", "Apellidos", "Email", "Nombre de usuario", "Nombre completo", "Contraseña"])
            for user in users:
                writer.writerow(user.toRow())
