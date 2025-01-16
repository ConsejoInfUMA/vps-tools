import secrets

class User:
    firstName: str
    lastName: str
    email: str
    identifier: str
    displayName: str
    password: str = None

    def __init__(self, firstName: str, lastName: str, email: str, identifier: str = None, displayName: str = None, autogen_password: bool = False):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

        if identifier is None:
            self.identifier = self.email.split('@')[0]
        else:
            self.identifier = identifier

        if displayName is None:
            self.displayName = f"{self.firstName} {self.lastName}"
        else:
            self.displayName = displayName
            
        if autogen_password:
            self.password = secrets.token_urlsafe(16)

    def __eq__(self, other): 
        return self.email == other.email
    
    def __hash__(self) -> int:
        return self.email.__hash__()
