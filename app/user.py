import enum



class Role(enum.Enum):
    ADMIN = "ROLE=ADMIN"
    USER = "ROLE=USER"
    ANONYMOUS = "ROLE=ANONYMOUS"

class CTSSUser:
    def __init__(self, credentials):
        self.__username, self.__password = credentials 

    @staticmethod
    def authenticate(credentials):
        username, password = credentials
        if username == "vivek" and password == "vivek":
            return True, Role.USER
        return False, Role.ANONYMOUS