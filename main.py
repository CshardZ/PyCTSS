from server.server import CTSSServer
from client.client import CTSSClient
from app.interface import Interface, UserInterface, AdminInterface
from app.user import CTSSUser
from auth.auth import Role



class PyCTSSApp:
    def __init__(self):
        self.user = CTSSUser('GUEST', 'GUEST')
        self.guest_client = CTSSClient(self.user)
        self.interface = Interface(self.guest_client)

    def client_mode(self, username, role):
        user = CTSSUser(username, role)
        client = CTSSClient(user)
        if role == Role.ADMIN.value:
            interface = AdminInterface(user, client)
        else:
            interface = UserInterface(user, client)
        interface.start()

    def server_mode(self):
        server = CTSSServer()
        server.start()

    def ask_app_mode(self):
        self.mode = input("Enter Application Mode - S or C: ").lower()

    def run(self):
        self.ask_app_mode()
        if self.mode == 'c':
            self.guest_client.connect_to_server()
            username, role = self.interface.authenticate()
            self.client_mode(username, role)
        else:
            self.server_mode()


if __name__ == '__main__':
    app = PyCTSSApp()
    app.run()