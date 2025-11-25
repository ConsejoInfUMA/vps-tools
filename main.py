from dotenv import load_dotenv
from sys import argv
from typing import List
from onboarding.helpers.Env import Env
from onboarding.models.User import User
from onboarding.Csv import Csv
from onboarding.Ldap import Ldap
from onboarding.Mail import Mail

def get_arg(argv: List[str], pos: int, default: str = None):
    return argv[pos] if pos < len(argv) else default

def add_user(ldap: Ldap, csv: Csv, mail: Mail, address: str):
    user = csv.getUserByEmail(address)
    if user is None:
        print('User not found')
        return

    ok = ldap.add(user)
    if not ok:
        return

    mail.sendWelcome(user)

def main(argv: List[str]):
    load_dotenv()

    ldap_url = Env.ldap_url()
    ldap_base_dn = Env.ldap_base_dn()
    ldap_username = Env.ldap_username()
    ldap_password = Env.ldap_password()

    ldap = Ldap(ldap_url, ldap_base_dn, ldap_username, ldap_password)

    mode = get_arg(argv, 1)

    if mode == 'add':
        # CSV class
        csv_path = Env.csv_path()
        csv_firstname = Env.csv_fistName_key()
        csv_lastname = Env.csv_lastName_key()
        csv_email = Env.csv_email_key()
        csv = Csv(csv_path, csv_firstname, csv_lastname, csv_email)

        # Email class
        mail_host = Env.mail_host()
        mail_port = Env.mail_port()
        mail_username = Env.mail_username()
        mail_password = Env.mail_password()
        mail_secure = Env.mail_secure()

        mail = Mail(mail_host, mail_port, mail_username, mail_password, mail_secure)
        address = get_arg(argv, 2)
        add_user(ldap, csv, mail, address)
    else:
        print('Invalid mode')
        return

if __name__ == "__main__":
    main(argv)
