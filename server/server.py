import socket
import threading
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
        self.sock.listen()
        print(self.ip, "SERVER STARTED\n")
        while True:
            client, addr = self.accept_connection()
            thread = threading.Thread(target=self.handle_client, args=(client))
            thread.start()

    def accept_connection(self):
        client, address = self.sock.accept()
        client_address = f"{address[0]}:{address[1]}"
        client_name = socket.gethostbyaddr(address[0])[0]
        print(f"[CONNECTION]: CTSSClient-{client_address}-{client_name}")
        handshake_request = self.receive(client)
        username = handshake_request['payload']
        self.clients[username] = client
        return client, address

    def handle_client(self, client):
        while True:
            request = self.receive(client)
            if request:
                packet = RequestHandler(request).handle_request()
                if packet:
                    client.send(packet)

    def receive(self, client):
        # TODO Cannot handle large data
        raw = client.recv(1024)
        data = None
        if raw:
            data = json.loads(raw.decode('utf-8'))
            print("[REQUEST]:", raw)
        return data


    def send(self, client, packet):
        client.send(packet)




class RequestHandler:

    def __init__(self, request):
        self.header = request['header']
        self.method = request['method']
        self.resource = request['resource']
        self.payload = request['payload']
        self.app_base_path = config.APP_BASE_PATH

        self._dispatch= {
            ("CREATE", "FILE"): self._create_file,
            ("READ", "FILE"): self._read_file,
            ("UPDATE", "FILE"): self._update_file,
            ("DELETE", "FILE"): self._delete_file,

            ("CREATE", "USER"): self._create_user,
            ("READ", "USER"): self._read_user,
            ("DELETE", "USER"): self._delete_user,
            
            ("CREATE", "ADMIN"): None,
            ("READ", "ADMIN"): None,
            ("DELETE", "ADMIN"): None,

            ("READ", "FOLDER"): self._read_folder,
            ("UPDATE", "FOLDER"): None,


            ("SHARE", "FILE"): self._share_file,
        }

    def handle_request(self):
        key = (self.method, self.resource)
        handler = self._dispatch.get(key, None)
        if handler:
            packet = handler()
            return packet

    def _create_file(self):
        file = self.app_base_path / self.header['path']
        file.touch()
    
    def _read_file(self):
        file_path = self.app_base_path / self.header['path']
        file_content = file_path.read_text()
        packet = util.serialize_packet("READ", "FILE", content=file_content)
        return packet

    def _update_file(self):
        file_path = self.app_base_path / self.header['path']
        file_path.touch()
        file_path.write_text(self.payload)

    def _delete_file(self):
        file_path = self.app_base_path / self.header['path']
        file_path.unlink()

    def _share_file(self):
        path = pathlib.Path(self.header['path'])
        file_name = path.name
        sender_path = self.app_base_path / path
        receiver_path = self.app_base_path / pathlib.Path(str(config.USER_FILES_PATH).format(self.payload)) / file_name
        receiver_path.touch()
        receiver_path.write_text(sender_path.read_text())

    def _read_folder(self):
        folder_path = self.app_base_path / self.header['path']
        folder_files = server_util.get_files_info(folder_path)
        packet = util.serialize_packet("READ", "FOLDER", content=folder_files)
        return packet
    
    def _create_user(self):
        auth.CTSSAuth.sign_up(self.payload)
        server_util.create_user_workspace(self.payload)

    def _read_user(self):
        verified = auth.CTSSAuth.sign_in(self.payload)
        return verified

    def _delete_user(self):
        auth.CTSSAuth.delete_account(self.payload)
        server_util.delete_user_workspace(self.payload)