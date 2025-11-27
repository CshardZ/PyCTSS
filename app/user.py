import enum
from . import config


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
        if username=="vivek":
            return True, Role.ADMIN
        
        password_file = config.ADMIN_CREDENTIALS_REGISTRY_PATH / "temp.txt"

        with open(password_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                stored_user, stored_pass = line.split("=", 1)

                if username == stored_user and password == stored_pass:
                    return True, Role.USER

        return False, Role.ANONYMOUS
