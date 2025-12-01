import socket
import threading
from . import server_util
import json
from util import util
from auth import auth
import pathlib
import config
from rich.logging import RichHandler
import logging
from datetime import datetime
import rich.console



class CTSSServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.clients = {}
        self.listening_address = (self.ip, config.SERVER_PORT)
        self.logger = ServerLogger(self.listening_address)

    def start(self):
        self.sock.bind(self.listening_address)
        self.sock.listen()
        self.logger.success("PyCTSS server started", 'SERVER')
        while True:
            client, addr = self.accept_connection()
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def accept_connection(self):
        client, address = self.sock.accept()
        self.logger.success("Incoming connection request", 'GUEST')
        return client, address

    def handle_client(self, client):
        while True:
            request = self.receive(client)
            if request:
                username = server_util.get_username_from(client, self.clients)
                if request['resource'] == 'HANDSHAKE':
                    self.clients[request['payload']] = client
                    self.logger.success("Connection successfull with handshake", username)

                elif request['resource'] == 'DISCONNECT':
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    self.clients.pop(request['payload'], None)
                    self.logger.success("Incoming disconnection request", username)
                    break
                else:
                    packet, log_status, log_message = RequestHandler(request).handle_request()
                    self.logger.log(log_status, log_message, username)
                    if packet:
                        client.send(packet)


    def receive(self, client):
        # TODO Cannot handle large data
        raw = client.recv(1024)
        data = None
        if raw:
            data = json.loads(raw.decode('utf-8'))
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
        if file.is_file():
            return None, 'FAILURE', f"File {file.name} already exists"
        else:
            file.touch()
            return None, 'SUCCESS', f"New file {file.name} created"
        


    def _read_file(self):
        file_path = self.app_base_path / self.header['path']
        if file_path.is_file():
            file_content = file_path.read_text()
            packet = util.serialize_packet("READ", "FILE", content=file_content)
            return packet, 'INFO', f"File {file_path.name} requested"
        else:
            return None, 'FAILURE', f"File {file_path.name} doesn't exist"


    def _update_file(self):
        file_path = self.app_base_path / self.header['path']
        if file_path.is_file():
            file_path.touch()
            file_path.write_text(self.payload)
            return None, 'INFO', f"File {file_path.name} got updated"
        else:
            return None, 'FAILURE', f"File {file_path.name} doesn't exist"


    def _delete_file(self):
        file_path = self.app_base_path / self.header['path']
        if file_path.is_file():
            file_path.unlink()
            return None, 'INFO', f"File {file_path.name} got deleted"
        else:
            return None, 'FAILURE', f"File {file_path.name} doesn't exist"


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
        return packet, None, None
    
    def _create_user(self):
        auth.CTSSAuth.create_account(self.payload)
        return None, None, None

    def _read_user(self):
        username, verified, role = auth.CTSSAuth.verify_sign_in(self.payload)
        packet = util.serialize_packet('READ', 'USER', content=(username, verified, role))
        return packet, None, None

    def _delete_user(self):
        auth.CTSSAuth.delete_account(self.payload)
        return None, None, None


class ServerLogger:
    def __init__(self, server_address,logger_name="PyCTSS"):
        self.logger_name = f"{logger_name} - {server_address}"
        self.console = rich.console.Console()
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        handler = RichHandler(
            console=self.console,
            rich_tracebacks=True,
            markup=True,
            show_time=False,      
            show_level=False,
            show_path=False
        )
        handler.setLevel(logging.INFO)
        # self.logger.handlers.clear()   # avoid duplicate logs
        self.logger.addHandler(handler)

    def log(self, log_status, log_message, username):
        if log_status == 'SUCCESS':
            self.success(log_message, username)
        elif log_status == 'FAILURE':
            self.failure(log_message, username)
        elif log_status == 'ERROR':
            self.error(log_message, username)
        elif log_status == 'INFO':
            self.info(log_message, username)

    def success(self, msg, username):
        status = "SUCCESS"
        client = f"Client({username})"
        now = datetime.now().strftime("%d-%b-%y %H:%M:%S")
        rich_msg = f"[{self.logger_name}][bold green] [{status:^10}][/bold green] [grey19]{now}[/grey19] - {client:<20} : [bold dark_blue]{msg}[/bold dark_blue]"
        self.logger.info(rich_msg, extra={"markup": True, 'highlighter':None})

    def failure(self, msg, username):
        status = "FAILURE"
        client = f"Client({username})"
        now = datetime.now().strftime("%d-%b-%y %H:%M:%S")
        rich_msg = f"[{self.logger_name}][bold yellow] [{status:^10}][/bold yellow] [grey19]{now}[/grey19] - {client:<20} : [bold dark_blue]{msg}[/bold dark_blue]"
        self.logger.info(rich_msg, extra={"markup": True, 'highlighter':None})

    def info(self, msg, username):
        status = "INFO"
        client = f"Client({username})"
        now = datetime.now().strftime("%d-%b-%y %H:%M:%S")
        rich_msg = f"[{self.logger_name}][bold blue] [{status:^10}][/bold blue] [grey19]{now}[/grey19] - {client:<20} : [bold dark_blue]{msg}[/bold dark_blue]"
        self.logger.info(rich_msg, extra={"markup": True, 'highlighter':None})

    def error(self, msg, username):
        status = "ERROR"
        client = f"Client({username})"
        now = datetime.now().strftime("%d-%b-%y %H:%M:%S")
        rich_msg = f"[{self.logger_name}][bold red] [{status:^10}][/bold red] [grey19]{now}[/grey19] - {client:<20} : [bold dark_blue]{msg}[/bold dark_blue]"
        self.logger.info(rich_msg, extra={"markup": True, 'highlighter':None})

# ServerLogger().success("some message", 'dinesh')
# ServerLogger().error("some message", 'ganesh')
# ServerLogger().failure("some message", 'rameshwar')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().success("some message", 'dinesh')
# ServerLogger().error("some message", 'ganesh')
# ServerLogger().failure("some message", 'rameshwar')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().success("some message", 'dinesh')
# ServerLogger().error("some message", 'ganesh')
# ServerLogger().failure("some message", 'rameshwar')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')
# ServerLogger().info("some message", 'gajju')