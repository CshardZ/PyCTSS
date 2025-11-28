import socket
import json # standard format


class CTSSClient:
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.last_response = None


    def send(self, message):
        encoded_message = message.encode('utf-8')
        self.sock.send(encoded_message)
        print("I sent a message bro")


    def receive(self):
        message = self.sock.recv(999_999)
        self.last_response = message


    def connect_to_server(self, server_ip="192.168.1.10", server_port=5000): # TODO need DNS resolver instead direct ip addresses lan.pyctss.app
        self.sock.connect((server_ip, server_port))


    def send_request(self, protocol, path, method="NONE", content="NONE"):
        request = f"{protocol}[SEP]{path}[SEP]{method}[SEP]{content}"
        self.send(request)


    def get_response(self, protocol):
        # format message based on protocol
        self.receive()
        if protocol == "FILES_LIST":
            data = json.loads(self.last_response.decode())
            return dict(data)
        elif protocol == "FILE_OBJ":
            return self.last_response