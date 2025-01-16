from os import getenv
from ceetsii.modules.Base import Base
from ceetsii.modules.Ldap import Ldap
from ceetsii.models import Option

class Entrypoint(Base):
    ldap: Ldap

    options: list[Option]

    def __init__(self):
        self.ldap = Ldap(
            base_url=getenv("LLDAP_BASE", "http://localhost:17170"),
            token=getenv("LLDAP_TOKEN", ""),
            out_dir=getenv("LLDAP_OUT", "out"),
            group_id=int(getenv("LLDAP_GROUP_ID", -1))
        )

        self.options = [
            Option(
                'LDAP',
                self.ldap.main
            )
        ]

    def run(self):
        self._pick(self.options, 'Elige el módulo que quieres usar')
