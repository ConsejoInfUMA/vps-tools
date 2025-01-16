import smtplib, ssl
from email.mime.text import MIMEText
from ceetsii.models.User import User

TEMPLATE = """
Hola {name},

Debido a que eres representante de la asignatura "{subject}", formas parte oficialmente del Consejo de Estudiantes.

¡Bienvenid@!

A todos los miembros del consejo se le genera una cuenta en nuestro servidor.

Tenemos disponibles los siguientes servicios:

- Nextcloud, disponible en {url}/nextcloud. Este es nuestro sitio principal de trabajo.

Éstas son tus credenciales:

Nombre de usuario: {username}
Contraseña: {password}

Puedes cambiar tu contraseña en {url}.
"""

TITLE = "¡Bienvenid@ al CEETSII!"

class Mail:
    server: str
    port: int
    username: str
    password: str
    base_url: str

    def __init__(self, server: str, port: int, username: str, password: str, base_url: str):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.base_url = base_url

    def sendWelcome(self, users: list[User]):
        server = smtplib.SMTP(self.server, self.port)
        if self.username != "" and self.password != "":
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(self.username, self.password)

        for user in users:
            msg = MIMEText(
                TEMPLATE.format(
                    name=user.displayName,
                    subject=user.subject,
                    url=self.base_url,
                    username=user.identifier,
                    password=user.password
                )
            )

            msg["Subject"] = "¡Bienvenido al CEETSII!"
            msg["From"] = self.username
            msg["To"] = user.email

            server.sendmail(
                self.username,
                user.email,
                msg.as_string()
            )

        server.quit()

        server.close()

