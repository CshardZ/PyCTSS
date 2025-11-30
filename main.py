from server.server import CTSSServer
from client.client import CTSSClient
from app.interface import Interface, UserInterface, AdminInterface
from app.user import CTSSUser



class PyCTSSApp:
    def __init__(self):
        self.interface = Interface()
        self.mode = "USER"

    def client_mode(self):
        # authenticate user or admin or anonymous then
        user = CTSSUser(('vivek', 'password'),'ADMIN')
        client = CTSSClient()
        # interface = AdminInterface(user, client)
        interface = UserInterface(user, client)
        interface.start()

    def server_mode(self):
        server = CTSSServer() # Should take a LOGGING Interface
        server.start()

    def ask_app_mode(self):
        self.mode = input("mode c or s: ")

    def run(self):
        if self.mode == 'c':
            self.client_mode()
        else:
            self.server_mode()




if __name__ == '__main__':
    app = PyCTSSApp()
    app.ask_app_mode()
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