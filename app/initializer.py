import pathlib
from app import config

from utils import generic


# Main Functions
# =======================================================================================
def create_app_dir():
    user_desktop = pathlib.Path.home() / config.DESKTOP_DIR
    app_dir = user_desktop / config.APP_DIR
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def create_default_dirs():
    app_path = generic.get_app_directory_path()
    
    user_dir = app_path / config.USERS_DIR
    admin_dir = app_path / config.ADMINS_DIR

    dirs = [
        user_dir / config.USER_PROFILE_DIR,
        user_dir / config.USER_FILES_DIR,
        user_dir / config.USER_SEETING_DIR
,
        admin_dir / config.LOGS_DIR,
        admin_dir / config.LOGS_DIR / config.USER_ACTIVITY_LOGS_DIR,
        admin_dir / config.LOGS_DIR / config.USER_SESSION_LOGS_DIR,
        admin_dir / config.LOGS_DIR / config.USER_FEEDBACK_LOGS_DIR,
    ]

    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)

# Testing
# =======================================================================================
if __name__ == '__main__':
    create_app_dir()
    create_default_dirs()
    
    pass