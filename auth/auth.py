import enum
from app import config
import rich.prompt
from util import util


class Role(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"
    ANONYMOUS = "ANONYMOUS"

    
class CTSSAuth:

    def __new__(cls, *args, **kwargs):
        raise TypeError("CTSSAuth is static only, cannot be instatiated")
    
    @classmethod
    def _authenticate(cls):
        pass

    @classmethod
    def _hash(cls, password):
        pass

    @classmethod
    def _store_credentials(cls, credentials):
        pass
    
    @classmethod
    def sign_up(cls, credentials):
        username, password = credentials
        password_file = config.ADMIN_CREDENTIALS_REGISTRY_PATH / "passwords.txt"
        with open(password_file, 'a') as f:
            f.write(f"{username}={password}\n")


    @classmethod
    def sign_in(cls, client):
        prompt = rich.prompt.Prompt()
        username = prompt.ask("Username")
        password = prompt.ask("Password")
        username, verified, role = client.read_user((username, password))
        return username, verified, role

    @classmethod
    def verify_sign_in(cls, credentials):
        username, password = credentials
        password_file = config.ADMIN_CREDENTIALS_REGISTRY_PATH / "passwords.txt"
        with open(password_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                stored_user, stored_pass = line.split("=", 1)

                if username == stored_user and password == stored_pass:
                    return username, True, Role.USER.value

        print("BRO FAILED", username, password)
        return username, False, Role.ANONYMOUS.value
    
    @classmethod
    def sign_out(cls):
        pass
    
    @classmethod
    def delete_account(cls, credentials):
        username, password = credentials
        password_file = config.ADMIN_CREDENTIALS_REGISTRY_PATH / "temp.txt"

        with open(password_file, 'r') as f:
            lines = f.readlines()

        with open(password_file, 'w') as f:
            for line in lines:
                if not line.strip():
                    continue

                stored_user, _ = line.strip().split("=", 1)
                if stored_user == username:
                    continue

                f.write(line)

    

    @classmethod
    def notify(cls):
        pass