import pathlib



# Base Paths
# =================================================================================================
SYSTEM_USER_PATH = pathlib.Path.home()
SYSTEM_USER_DESKTOP_PATH = SYSTEM_USER_PATH / "Desktop"


# App Configs
# =================================================================================================
APP_LOGO = """

███████████               █████████   ███████████  █████████   █████████ 
░░███░░░░░███            ███░░░░░███░░█░░░███░░░█ ███░░░░░███ ███░░░░░███
 ░███    ░███ █████ ████ ███     ░░░ ░   ░███  ░ ░███    ░░░ ░███    ░░░ 
 ░██████████ ░░███ ░███ ░███             ░███    ░░█████████ ░░█████████ 
 ░███░░░░░░   ░███ ░███ ░███             ░███     ░░░░░░░░███ ░░░░░░░░███
 ░███         ░███ ░███ ░░███     ███    ░███     ███    ░███ ███    ░███
 █████        ░░███████  ░░█████████     █████   ░░█████████ ░░█████████ 
░░░░░          ░░░░░███   ░░░░░░░░░     ░░░░░     ░░░░░░░░░   ░░░░░░░░░  
...............███ ░███..................................................                                                  
..............░░██████...................................................
...............░░░░░░....................................................

"""

APP_NAME = 'PyCTSS'
APP_BASE_PATH = SYSTEM_USER_DESKTOP_PATH / APP_NAME
RICH_STANDARD_COLORS = [
    "bright_blue", "bright_magenta", "bright_cyan"
    "bright_red", "bright_green", "bright_yellow",
    "black", "red", "green", "yellow", "blue",
    "magenta", "cyan", "white", "bright_black",
]

PROMPT_STYLE = "[bold blue3]Command: [/bold blue3]"



# Server Configs
# =================================================================================================
SERVER_DOMAIN_NAME = "lan.pyctss.app"
SERVER_PORT = 5000
# SERVER_IP = DNS(SERVER_DOMAIN_NAME)

ALL_USERS_PATH = APP_BASE_PATH / "USERS"
ALL_ADMINS_PATH = APP_BASE_PATH / "ADMINS"
ADMIN_PASSWORDS_PATH = ALL_ADMINS_PATH / "Passwords-Registry" / 'admin-passwords.txt'
USER_PASSWORDS_PATH = ALL_ADMINS_PATH / "Passwords-Registry" / 'user-passwords.txt'
CHATS_PATH = ALL_USERS_PATH / "Chats"

USER_PATH = ALL_USERS_PATH / "{}"
USER_FILES_PATH = USER_PATH / "Files"



# Client Configs
# =================================================================================================
CLIENT_WORKING_DIRECTORY_PATH = SYSTEM_USER_DESKTOP_PATH / "PyCTSSClient"
CLIENT_RELATIVE_ADMINS_PATH = pathlib.Path('ADMINS/')
CLIENT_RELATIVE_USERS_PATH = pathlib.Path('Users/{}')