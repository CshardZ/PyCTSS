from . import app_util

def initialize(app_mode):
    if app_mode == 'server':
        app_util.create_server_dirs()
    if app_mode == 'client':
        app_util.create_client_dirs()