import enum



class Role(enum.Enum):
    ADMIN = "ROLE=ADMIN"
    USER = "ROLE=USER"
    ANONYMOUS = "ROLE=ANONYMOUS"

class CTSSUser:
    def __init__(self, credentials, role):
        self.username = credentials[0] 
        self.__password = credentials[1]
        self.role = role

    @staticmethod
    def authenticate(credentials):
        username, password = credentials
        if username == "vivek" and password == "vivek":
            # return True, Role.USER
            return True, Role.ADMIN
        return False, Role.ANONYMOUS