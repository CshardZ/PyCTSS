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


SERVER_USER_HOME_PATH = pathlib.Path.home()

SERVER_USER_DESKTOP_DIR_NAME = "Desktop"
SERVER_USER_DESKTOP_PATH = SERVER_USER_HOME_PATH / SERVER_USER_DESKTOP_DIR_NAME

APP_BASE_DIR_NAME = "PyCTSS"
APP_BASE_PATH = SERVER_USER_DESKTOP_PATH / APP_BASE_DIR_NAME

ALL_USERS_DIR_NAME = "Users"
APP_USERS_PATH = APP_BASE_PATH / ALL_USERS_DIR_NAME

ALL_ADMINS_DIR_NAME = "Admins"
APP_ADMINS_PATH = APP_BASE_PATH / ALL_ADMINS_DIR_NAME

USER_PERSONAL_DIR_NAME = "{}"
USER_PERSONAL_PATH = APP_USERS_PATH / USER_PERSONAL_DIR_NAME

ADMIN_PERSONAL_DIR_NAME = "{}"
ADMIN_PERSONAL_PATH = APP_ADMINS_PATH / ADMIN_PERSONAL_DIR_NAME

USER_PERSONAL_FILES_DIR_NAME = "Files"
USER_PERSONAL_PROFILE_DIR_NAME = "Profile"
USER_PERSONAL_SETTING_DIR_NAME = "Setting"

USER_PERSONAL_FILES_PATH = USER_PERSONAL_PATH / USER_PERSONAL_FILES_DIR_NAME
USER_PERSONAL_PROFILE_PATH = USER_PERSONAL_PATH / USER_PERSONAL_PROFILE_DIR_NAME
USER_PERSONAL_SETTING_PATH = USER_PERSONAL_PATH / USER_PERSONAL_SETTING_DIR_NAME





RICH_COLORS = ["bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan"]