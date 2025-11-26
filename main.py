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
    # TODO !important Have to start the central server first!
    interface = Interface()
    interface.show_splash_screen()
    print("START")
    credentials = interface.prompt_login_credentials()
    verified, role = CTSSUser.authenticate(credentials)
    if verified:
        if role == Role.ADMIN:
            admin_user = CTSSUser(credentials, role)
            return AdminInterface(admin_user)
        if role == Role.USER:
            normal_user = CTSSUser(credentials, role)
            return UserInterface(normal_user)
        if role == Role.ANONYMOUS:
            raise PermissionError("Access Denied: Role Unidentified")
    
    raise PermissionError("Access Denied: Verfication Unsuccessfull")


def work(userinterface):
    userinterface.home()

setup()
userinterface = start()
work(userinterface)