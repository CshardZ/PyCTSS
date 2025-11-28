import pathlib

"""
App Directory Structure

PyCTSS
    |-- Users
        |-- User 1
            |-- Files
            |-- Profile
            |-- Setting
        |-- User 2
            |-- Files
            |-- Profile
            |-- Setting
        |-- User N
            |-- Files
            |-- Profile
            |-- Setting

    |-- Admins
        |-- Admins
            |-- Admin 1
            |-- Admin 2
            |-- Admin N
        |-- Logs
            |-- User Logs
                |-- User Session Logs
                |-- User Activity Logs
                |-- User Tresspass Logs
            |-- Admin Logs
            |-- Server Logs
            |-- Reports
"""


SYSTEM_USER_PATH = pathlib.Path.home()
SYSTEM_USER_DESKTOP_PATH = SYSTEM_USER_PATH / "Desktop"

CLIENT_TEMP_FOLDER_PATH = SYSTEM_USER_PATH / "PyCTSSClient"


CLIENT_SIDE_RELATIVE_ADMINS = pathlib.Path("ADMINS/")

APP_NAME = "PyCTSS"
APP_BASE_PATH = SYSTEM_USER_DESKTOP_PATH / APP_NAME

ALL_USERS_PATH = APP_BASE_PATH / "USERS"
ALL_ADMINS_PATH = APP_BASE_PATH / "ADMINS"
ADMIN_CREDENTIALS_REGISTRY_PATH = ALL_ADMINS_PATH / "Credentials-Registry"

USER_PERSONAL_PATH = ALL_USERS_PATH / "{}"
USER_FILES_PATH = USER_PERSONAL_PATH / "Files"




RICH_STANDARD_COLORS = [
    "bright_blue", "bright_magenta", "bright_cyan"
    "bright_red", "bright_green", "bright_yellow",
    "black", "red", "green", "yellow", "blue",
    "magenta", "cyan", "white", "bright_black",
]

PROMPT_STYLE = "[bold blue3]Command: [/bold blue3]"

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