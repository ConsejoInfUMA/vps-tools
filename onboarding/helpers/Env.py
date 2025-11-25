from os import environ

class Env:
    @staticmethod
    def ldap_url() -> str:
        return environ.get('LDAP_URL', 'ldap://127.0.0.1:389')

    @staticmethod
    def ldap_base_dn() -> str:
        return environ.get('LDAP_BASE_DN', '')

    @staticmethod
    def ldap_username() -> str:
        return environ.get('LDAP_USERNAME', '')

    @staticmethod
    def ldap_password() -> str:
        return environ.get('LDAP_PASSWORD', '')

    @staticmethod
    def csv_path() -> str:
        return environ.get('CSV_PATH', 'data.csv')

    @staticmethod
    def csv_fistName_key() -> str:
        return environ.get('CSV_FIRSTNAME_KEY')

    @staticmethod
    def csv_lastName_key() -> str:
        return environ.get('CSV_LASTNAME_KEY')

    @staticmethod
    def csv_email_key() -> str:
        return environ.get('CSV_EMAIL_KEY')

    @staticmethod
    def mail_host() -> str:
        return environ.get('MAIL_HOST', 'localhost')

    @staticmethod
    def mail_port() -> int:
        return int(environ.get('MAIL_PORT', 1025))

    @staticmethod
    def mail_username() -> str:
        return environ.get('MAIL_USERNAME')

    @staticmethod
    def mail_password() -> str:
        return environ.get('MAIL_PASSWORD')

    @staticmethod
    def mail_secure() -> str:
        return environ.get('MAIL_SECURE', 'none')
