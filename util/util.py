import config
import json
from copy import deepcopy
from datetime import datetime

# Socket Communication Protocol Format
SCP_FORMAT = {
    'header': {
        'client_address': None,
        'server_address': None,
        'path': None
    },
    'method': None, # CREATE / READ / UPDATE / DELETE / SHARE
    'resource': None, # FILE / FOLDER / USER / ADMIN
    'payload': None
}

def serialize_packet(method, resource, sender=None, sender_path=None, content=None):
    msg = deepcopy(SCP_FORMAT)

    msg['header']['path'] = sender_path
    msg['method'] = method
    msg['resource'] = resource
    msg['payload'] = content

    return json.dumps(msg).encode("utf-8")


def deserialize_packet(packet):
    return json.loads(packet.decode('utf-8'))


def app_base_dir_exists():
    return config.APP_BASE_PATH.is_dir()

def format_chat_message(username, message):
    # [28-Jul-19 | 09:15pm]
    ts = datetime.now().strftime("[ %d-%b-%y | %I:%M %p ]")
    padded_user = f"({username:^10})"
    return f"{ts} — {padded_user} : {message}\n"