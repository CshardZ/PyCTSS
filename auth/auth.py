import enum
import rich.prompt
from . import auth_util
import config


class Role(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"
    ANONYMOUS = "ANONYMOUS"

    
class CTSSAuth:

    def __new__(cls, *args, **kwargs):
        raise TypeError("CTSSAuth is static only, cannot be instatiated")
    
    @classmethod
    def initiate_user_creation(cls, client):
        prompt = rich.prompt.Prompt()
        new_username = prompt.ask("Username")
        new_password = prompt.ask("New Password")
        confirm_password = prompt.ask("Confirm Password")
        if new_password == confirm_password:
            client.create_user((new_username, new_password))
        else:
            raise Exception("Task Failed: Passwords don't match")

    @classmethod
    def create_account(cls, credentials):
        new_username, new_password = credentials
        password_file = config.USER_PASSWORDS_PATH
        with open(password_file, 'a') as f:
            f.write(f"{new_username}={new_password}\n")
        auth_util.create_user_workspace(new_username)

    @classmethod
    def initiate_user_deletion(cls, client):
        prompt = rich.prompt.Prompt()
        username = prompt.ask("Username")
        client.delete_user(username)

    @classmethod
    def delete_account(cls, username):
        password_file = config.USER_PASSWORDS_PATH

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

        auth_util.delete_user_workspace(username)    

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
        user_passwords = config.USER_PASSWORDS_PATH
        admin_passwords = config.ADMIN_PASSWORDS_PATH

        with open(user_passwords, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                stored_user, stored_pass = line.split("=", 1)
                if username == stored_user and password == stored_pass:
                    return username, True, Role.USER.value #TODO Admin or User pendings
        
        with open(admin_passwords, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                stored_user, stored_pass = line.split("=", 1)
                if username == stored_user and password == stored_pass:
                    return username, True, Role.ADMIN.value #TODO Admin or User pendings

        return username, False, Role.ANONYMOUS.value
    

    @classmethod
    def sign_out(cls):
        pass
    

    @classmethod
    def notify(cls):
        pass