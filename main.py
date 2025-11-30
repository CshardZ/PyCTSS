from server.server import CTSSServer
from client.client import CTSSClient
from app.interface import Interface, UserInterface, AdminInterface
from app.user import CTSSUser



class PyCTSSApp:
    def __init__(self):
        self.user = CTSSUser('GUEST', 'GUEST')
        self.guest_client = CTSSClient(self.user)
        self.interface = Interface(self.guest_client)


    def client_mode(self, username, role):
        user = CTSSUser(username, role)
        client = CTSSClient(user)
        interface = AdminInterface(user, client)
        # interface = UserInterface(user, client)
        interface.start()

    def server_mode(self):
        server = CTSSServer() # Should take a LOGGING Interface
        server.start()

    def ask_app_mode(self):
        self.mode = input("mode c or s: ")

    def authenticate(self):
        username, verified, role = self.interface.authenticate()
        if not verified:
            raise Exception("Verification Failed: Wrong username or password")
        return username, verified, role

    def run(self):
        self.ask_app_mode()
        if self.mode == 'c':
            self.guest_client.connect_to_server()
            username, _, role = self.authenticate()
            self.client_mode(username, role)
        else:
            self.server_mode()




if __name__ == '__main__':
    app = PyCTSSApp()
    app.run()

"""
1. Run as Server/Client
    IF Server THEN 
        - setup centeral server
        - setup threading
        - start listening

    IF Client THEN Authentication(admin/user)
        - Ensure server running else provide proper message that server is down
        - Connect to server automatically on auth verification
        - Ensure client can communicate concurrently while others are also communicating
        - Start working
"""