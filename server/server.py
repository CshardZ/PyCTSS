import socket
import threading
import time
from app import config
from . import server_util
import json # standard format for data serialization


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
            client, addr = self.accept_connection()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            # IMP TODO get the username bound to the address, need it for serving personal files
            thread.start()
            # Above mechanism will create destroy multiple threads per client per task as client requests
            # Check if the thread can be kept alive till client request END CONNECTION
            # manage all tasks in task stack something like that.
            print("Active Clients: ", threading.active_count()-1)            

    def get_files(self, request):
        pass


    def handle_client(self, client, addr):
        while True:
            request = self.receive(client)
            if request:
                if request.split("[SEP]")[0] == "FILES_LIST":
                    dir_path = config.APP_BASE_PATH / request.split("[SEP]")[1]
                    print("Ppath is",dir_path, "app base is:", config.APP_BASE_PATH)
                    payload = self.get_files_list(dir_path)
                    client.send(payload)
                break

    def listen(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen()
        print(self.ip,"Server Started, now listening...")

    def stop(self):
        self.sock.close()
        print("Server Stopped")

    def get_files_list(self, dir_path):
        data = server_util.get_files_info(dir_path)
        payload = json.dumps(data).encode()
        return payload

    def accept_connection(self):
        client, address = self.sock.accept()
        """
        Got Connection Request From:  <socket.socket fd=588, family=2, type=1, proto=0, laddr=('192.168.1.10', 5000), raddr=('192.168.1.10', 60750)> ('192.168.1.10', 60750)
        """
        client_address = f"{address[0]}:{address[1]}"
        client_name = socket.gethostbyaddr(address[0])[0]
        print(f"Incoming Connection Request From: CTSSClient-{client_address}-{client_name}")
        return client, address


    def receive(self, client):
        # TODO Implement length prefixed framming for message transmission
        data = client.recv(1024).decode('utf-8')
        print("SERVER:Message Received: ", data)
        return data


    def send(self):
        pass