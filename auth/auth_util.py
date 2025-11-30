from app import config


def create_user_workspace(username):
    dirs = [
        config.ALL_USERS_PATH / username / "Files",
        config.ALL_USERS_PATH / username / "Shared",
        config.ALL_USERS_PATH / username / "Profile",
        config.ALL_USERS_PATH / username / "Setting",
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)

def delete_user_workspace(username):
    import shutil
    shutil.rmtree(config.ALL_USERS_PATH / username)