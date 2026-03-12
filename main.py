from server.server import CTSSServer
from client.client import CTSSClient
from app.interface import Interface, UserInterface, AdminInterface
from app.user import CTSSUser
from app.initializer import initialize
from auth.auth import Role


class PyCTSSApp:
    def __init__(self):
        self.user = CTSSUser('GUEST', 'GUEST')
        self.guest_client = CTSSClient(self.user)
        self.interface = Interface(self.guest_client)
        self.interface.screen.clear()
        self.mode = None
        self.server_ip = None
        self.server_port = None

    def client_mode(self, username, role):
        user = CTSSUser(username, role)
        client = CTSSClient(user, self.server_ip, self.server_port)
        if role == Role.ADMIN.value:
            interface = AdminInterface(user, client)
        else:
            interface = UserInterface(user, client)
        interface.start()

    def server_mode(self):
        server = CTSSServer()
        server.start()

    def ask_app_mode(self):
        user_input = input("Enter Application Mode\n\t1 - Client\n\t2 - Server\nChoose (1 or 2): ")
        if user_input == '1':
            self.mode = 'client'
        elif user_input == '2':
            self.mode = 'server'

    def run(self):
        self.ask_app_mode()
        initialize(self.mode)
        if self.mode == 'client':
            self.interface.screen.clear()
            self.server_ip = input("\nEnter Server IP   : ")
            self.server_port = int(input("Enter Server port : "))
            self.guest_client.connect_to_server(self.server_ip, self.server_port)
            username, role = self.interface.authenticate()
            if username:
                self.client_mode(username, role)
        elif self.mode == 'server':
            self.interface.screen.clear()
            self.server_mode()
        else:
            print("Selected option is invalid")
        print('PyCTSS Application Ended')

if __name__ == '__main__':
    app = PyCTSSApp()
    app.run()