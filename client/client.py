import socket


class CTSSClient:
    
    def __init__(self, username, password):
        self.__username = username
        self.__password = password #TODO maintain hash table for all passwords
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)

    def connect(self, server_ip="192.168.1.10", server_port="5000"): # TODO need DNS resolver instead direct ip addresses lan.pyctss.app
        self.sock.connect((server_ip, server_port))

    def send(self, message):
        encoded_message = message.encode('utf-8')
        self.sock.send(encoded_message)

    def send_file(self, file_path):
        pass

    def receive(self):
        message = self.sock.recv(1024)
        decoded_message = message.decode('utf-8')