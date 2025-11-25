from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from string import Template
from onboarding.models.User import User
from onboarding.helpers.MLStripper import MLStripper

class Mail:
    client: smtplib.SMTP
    sender: str
    template: str

    def __init__(self, host: str, port: int, username: str, password: str, secure: str):
        self.sender = username
        with open('templates/welcome.html', 'r') as f:
            self.template = f.read()

        context = ssl.create_default_context()
        self.client = smtplib.SMTP(host, port)

        if secure == 'starttls':
            self.client.starttls(context=context)

        if username is not None and password is not None:
            self.client.login(username, password)

    def sendWelcome(self, user: User):
        message = MIMEMultipart("alternative")
        message["Subject"] = "¡Bienvenid@ al CEETSII!"
        message["From"] = self.sender
        message["To"] = user.email

        html = Template(self.template).safe_substitute({
            "firstName": user.firstName,
            "username": user.username,
            "email": user.email,
            "password": user.password,
        })

        s = MLStripper()
        s.feed(html)
        text = s.get_data()

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        self.client.sendmail(self.sender, user.email, message.as_bytes())

    def close(self):
        self.client.close()
