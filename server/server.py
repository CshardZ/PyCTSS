import socket


class CTSSServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)


    def start(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen(5)
        print(self.ip, "Server started, now listening...")
        while True:
            client, addr = self.accept_client()
            print("CONNECTED")
            self.handle_client(client, addr)
            

    def handle_client(self, client, addr):
        """with client:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                client.sendall(data)  # echo back"""

    def listen(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen()
        print(self.ip,"Server Started, now listening...")

    def stop(self):
        self.sock.close()
        print("Server Stopped")


    def accept_client(self):
        # TODO Implement thread per client, better use server_util.py for threading instead using global util for this
        client, address = self.sock.accept()
        """
        Got Connection Request From:  <socket.socket fd=588, family=2, type=1, proto=0, laddr=('192.168.1.10', 5000), raddr=('192.168.1.10', 60750)> ('192.168.1.10', 60750)
        """
        client_ip = address[0]
        client_name = socket.gethostbyaddr(client_ip)[0]
        print(f"Incoming Connection Request From: {client_name}{address}")
        return client, address


    def receive(self, client):
        # TODO Implement length prefixed framming for message transmission
        data = client.recv(1024).decode('utf-8')
        print(data)


    def send(self):
        pass