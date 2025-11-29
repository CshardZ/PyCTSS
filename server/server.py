import socket
import threading
import time
from app import config
from . import server_util
import json
from util import util
from auth import auth
import pathlib


class CTSSServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.clients = {}


    def start(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen(5)
        print(self.ip, "SERVER STARTED, Listening...\n\n")
        while True:
            client, addr = self.accept_connection()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            # handshake basically for getting username as payload
            handshake_request = self.receive(client)
            username = handshake_request['payload']
            self.clients[username] = client
            thread.start()


    def handle_client(self, client, addr):
        while True:
            request = self.receive(client)
            if request:
                header = request['header']
                method = request['method']
                resource = request['resource']
                payload = request['payload']

                if method == "CREATE":
                    if resource == "FILE":
                        file = config.APP_BASE_PATH / header['path'] / payload
                        file.touch()
                    if resource == "USER":
                        auth.CTSSAuth.sign_up(payload)
                        server_util.create_user_workspace(payload) # only username enough, payload consists both credentials
                    if resource == "ADMIN":
                        auth.CTSSAuth.sign_up(payload)
                
                elif method == "READ":
                    if resource == "FILE":
                        file = config.APP_BASE_PATH / header['path']
                        file_content = file.read_text()
                        packet = util.serialize_packet("READ", "FILE", content=file_content)
                        self.send(client, packet)

                    if resource == "FOLDER":
                        folder_path = config.APP_BASE_PATH / header['path']
                        folder_files = self.get_files_list(folder_path)
                        packet = util.serialize_packet("READ", "FOLDER", content=folder_files)
                        self.send(client, packet)
                    if resource == "USER":
                        verified = auth.CTSSAuth.sign_in(payload)
                    if resource == "ADMIN":
                        verified = auth.CTSSAuth.sign_in(payload)
                
                elif method == "UPDATE":
                    if resource == "FILE":
                        file = config.APP_BASE_PATH / header['path']
                        file.touch()
                        file.write_text(payload)
                    elif resource == "FOLDER":
                        # NOTE Feature not planned
                        pass

                elif method == "DELETE":
                    if resource == "FILE":
                        file = config.APP_BASE_PATH / header['path'] / payload
                        file.unlink()
                    if resource == "USER":
                        auth.CTSSAuth.delete_account(payload)
                        server_util.delete_user_workspace(payload)
                    if resource == "ADMIN":
                        auth.CTSSAuth.delete_account(payload)

                elif method == "SHARE":
                    if resource == "FILE":
                        receiver_username, file_name = payload
                        sender_path, receiver_path = header['path'].strip("()").split(',')
                        print("PRINTING PATH:", sender_path, receiver_path, pathlib.Path(sender_path), pathlib.Path(receiver_path))
                        file = config.APP_BASE_PATH / sender_path.strip("'") / file_name
                        file_content = file.read_text()
                        receiver_file = config.APP_BASE_PATH / pathlib.Path(receiver_path.strip("' ")) / file_name
                        receiver_file.write_text(file_content)
                        print("time.sleep(20), after this its infinite why?")
                        time.sleep(20)

    def listen(self):
        self.sock.bind((self.ip, 5000))
        self.sock.listen()
        print(self.ip,"Server Started, now listening...")

    def stop(self):
        self.sock.close()
        print("Server Stopped")

    def get_files_list(self, dir_path):
        data = server_util.get_files_info(dir_path)
        # payload = json.dumps(data).encode()
        return data

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
        raw = client.recv(1024)
        data = None
        if raw:
            data = json.loads(raw.decode('utf-8'))
        print("SERVER:Message Received: No Block?: ", raw)
        return data


    def send(self, client, packet):
        client.send(packet)