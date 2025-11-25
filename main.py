from server.server import CTSSServer
from client.client import CTSSClient
from util import util
from app import app_util
from app.interface import Interface, UserInterface, AdminInterface
from app.user import CTSSUser, Role


def setup():
    app_util.create_base_dirs()
    if not util.app_base_dir_exists():
        pass

def start():
    interface = Interface()
    interface.show_splash_screen()
    credentials = interface.show_login()
    verified, role = CTSSUser.authenticate(credentials)
    if verified:
        if role == Role.ADMIN:
            return AdminInterface()
        if role == Role.USER:
            print(role)
            return UserInterface()
        if role == Role.ANONYMOUS:
            raise PermissionError("Access Denied: Role Unidentified")
    
    raise PermissionError("Access Denied: Verfication Unsuccessfull")


start()