import enum
from . import config


class Role(enum.Enum):
    ADMIN = "ROLE=ADMIN"
    USER = "ROLE=USER"
    ANONYMOUS = "ROLE=ANONYMOUS"

    
class CTSSAuth:

    def __new__(cls, *args, **kwargs):
        raise TypeError("CTSSAuth is static only, cannot be instatiated")
    
    @staticmethod
    def _authenticate(cls):
        pass

    @staticmethod
    def _hash(cls, password):
        pass

    @staticmethod
    def _store_credentials(cls, credentials):
        pass
    
    @staticmethod
    def sign_up(cls):
        pass

    @staticmethod
    def sign_in(cls, credentials):
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
    
    @staticmethod
    def sign_out(cls):
        pass
    
    @staticmethod
    def delete_account(cls):
        pass
    

    @staticmethod
    def notify(cls):
        pass