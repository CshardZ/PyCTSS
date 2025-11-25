import socket



class CTSSServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)

    def start(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen()
        print(self.ip,"Server Started, now listening...")

    def stop(self):
        self.sock.close()
        print("Server Stopped")

    def accept_client(self):
        # TODO Implement thread per client, better use server_util.py for threading instead using global util for this
        client, address = self.sock.accept()
        return client, address

    def receive(self, client):
        # TODO Implement length prefixed framming for message transmission
        data = client.recv(1024).decode('utf-8')
        print(data)

    def send(self):
        pass