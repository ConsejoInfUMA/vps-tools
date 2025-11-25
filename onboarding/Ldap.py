import ldap
import ldap.modlist as modlist
from .models.User import User

class Ldap:
    client: ldap.ldapobject.SimpleLDAPObject
    baseDn: str

    def __init__(self, url: str, baseDn: str, username: str, password: str):
        self.baseDn = baseDn

        # Connect
        self.client = ldap.initialize(url)
        self.client.protocol_version = ldap.VERSION3

        # Auth
        self.client.simple_bind_s(self._buildUserDn(username), password)

    def add(self, user: User) -> bool:
        firstNameBytes = user.firstName.encode('utf-8')
        lastNameBytes = user.lastName.encode('utf-8')
        fullNameBytes = user.getFullName().encode('utf-8')
        usernameBytes = user.username.encode('utf-8')
        emailBytes = user.email.encode('utf-8')

        attrs = {
            'objectClass': [b'person'],
            'uid': [usernameBytes],
            'cn': [fullNameBytes],
            'givenName': [firstNameBytes],
            'sn': [lastNameBytes],
            'mail': [emailBytes],
            'user_id': [usernameBytes],
        }

        user_dn = self._buildUserDn(user.username)

        try:
            ldif = modlist.addModlist(attrs)
            self.client.add_s(user_dn, ldif)
            self.client.passwd_s(user_dn, '', user.password.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Failed to create user {user}: {repr(e)}")
            return False

    def _buildUserDn(self, username: str) -> str:
        return f"uid={username},{self.baseDn}"
