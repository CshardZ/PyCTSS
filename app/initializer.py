import pathlib
from utils import variables

from utils import generic


# Main Functions
# =======================================================================================
def create_app_dir():
    user_desktop = pathlib.Path.home() / variables.DESKTOP_DIR
    app_dir = user_desktop / variables.APP_DIR
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def create_default_dirs():
    app_path = generic.get_app_directory_path()
    
    user_dir = app_path / variables.USERS_DIR
    admin_dir = app_path / variables.ADMINS_DIR

    dirs = [
        user_dir / variables.USER_PROFILE_DIR,
        user_dir / variables.USER_FILES_DIR,
        user_dir / variables.USER_SEETING_DIR
,
        admin_dir / variables.LOGS_DIR,
        admin_dir / variables.LOGS_DIR / variables.USER_ACTIVITY_LOGS_DIR,
        admin_dir / variables.LOGS_DIR / variables.USER_SESSION_LOGS_DIR,
        admin_dir / variables.LOGS_DIR / variables.USER_FEEDBACK_LOGS_DIR,
    ]

    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)

# Testing
# =======================================================================================
if __name__ == '__main__':
    create_app_dir()
    create_default_dirs()
    
    pass