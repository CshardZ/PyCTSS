import socket



class CTSSServer:
    def __init__(self): # TODO enforce TEXT or FILE mode, can use ENUMs here if suitable
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.mode = None

    def start(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen()
        print("Server Started, now listening...")

    def stop(self):
        self.sock.close()
        print("Server Stopped")

    def accept_client(self):
        # TODO Implement thread per client, better use server_util.py for threading instead using global util for this
        client, address = self.sock.accept()
        return client, address

    def handle_client(self, client):
        # TODO Implement length prefixed framming for message transmission
        data = client.recv(1024).decode('utf-8')
        print(data)