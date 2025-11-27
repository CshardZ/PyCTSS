from server.server import CTSSServer
from client.client import CTSSClient
from app.interface import Interface, UserInterface, AdminInterface
from app.user import CTSSUser, Role



class PyCTSSApp:
    def __init__(self):
        self.interface = Interface()
        self.mode

    def client_mode(self, interface):
        client = CTSSClient(interface)
        client.start_working()

    def server_mode(self, interface):
        server = CTSSServer(interface)
        pass

    def ask_app_mode(self):
        # Client or Server ?
        pass

    def run(self):
        pass




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