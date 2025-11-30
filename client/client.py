import socket
from util import util
from app import config

class CTSSClient:
    
    def __init__(self, user):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.working_path = config.CLIENT_TEMP_FOLDER_PATH
        self.user = user

    def connect_to_server(self, server_ip="192.168.1.10", server_port=5000): 
        # TODO need DNS resolver instead direct ip addresses lan.pyctss.app
        self.sock.connect((server_ip, server_port))
        # Handshake with username
        request = util.serialize_packet(
            method = "NONE",
            resource = "NONE",
            content = self.user.username,
        )
        self.sock.send(request)


    def _send(self, method, resource, path=None, content=None):
        request = util.serialize_packet(
            method = method,
            resource = resource,
            content = content,
            sender = self.ip,
            sender_path = str(path),
        )
        self.sock.send(request)

    def _receive(self):
        packet = self.sock.recv(999_999)
        response = util.deserialize_packet(packet)
        header = response['header']
        method = response['method']
        resource = response['resource']
        payload = response['payload']

        return payload


    def create_file(self, path):
        self._send('CREATE', 'FILE', path)

    def read_file(self, path):
        self._send('READ', 'FILE', path)
        data = self._receive()
        temp_file = self.working_path / 'temp.txt'
        temp_file.touch()
        temp_file.write_text(data)
        return temp_file

    def update_file(self, path, content):
        self._send('UPDATE', 'FILE', path, content)

    def delete_file(self, path):
        self._send('DELETE', 'FILE', path)

    def share_file(self, path, receiver):
        self._send('SHARE', 'FILE', path, receiver)


    def read_folder(self, path):
        self._send('READ', 'FOLDER', path)
        data = self._receive()
        return data
    
    
    def create_user(self, credentials):
        self._send('CREATE', 'USER', content = credentials)
    
    def read_user(self, credentials):
        self._send('READ', 'USER', content = credentials)
        data = self._receive()
        return data
    
    def delete_user(self, username):
        self._send('DELETE', 'USER', content = username)