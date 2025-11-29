from datetime import datetime
from app import config


def get_files_info(path):
    files_info = {}
    for index, file in enumerate(path.iterdir(), start=1):
        stats = file.stat()
        files_info[index] = {
            'name': file.name,
            'size': f"{stats.st_size // 1024} Kb",
            'created': datetime.fromtimestamp(stats.st_birthtime).strftime("%Y.%m.%d %H:%M:%S"),
            'updated': datetime.fromtimestamp(stats.st_mtime).strftime("%Y.%m.%d %H:%M:%S")
        }
    return files_info


def create_user_workspace(credentials):
    username, _ = credentials
    dirs = [
        config.ALL_USERS_PATH / username / "Files",
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)

def delete_user_workspace(credentials):
    import shutil
    username, _ = credentials
    shutil.rmtree(config.ALL_USERS_PATH / username)