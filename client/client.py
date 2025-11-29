import socket
import json # standard format
from util import util


class CTSSClient:
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)

    def connect_to_server(self, server_ip="192.168.1.10", server_port=5000): 
        # TODO need DNS resolver instead direct ip addresses lan.pyctss.app
        self.sock.connect((server_ip, server_port))

    def send(self, method, resource, path="NONE", content="NONE"):
        request = util.serialize_packet(
            method = method,
            resource = resource,
            content = content,
            sender = self.ip,
            sender_path = str(path),
        )
        self.sock.send(request)

    def receive(self):
        packet = self.sock.recv(999_999)
        response = util.deserialize_packet(packet)
        header = response['header']
        method = response['method']
        resource = response['resource']
        payload = response['payload']

        if resource == "FILE":
            return payload
        elif resource == "FOLDER":
            return payload
