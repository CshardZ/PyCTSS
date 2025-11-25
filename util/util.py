import pathlib
from app import config


def app_base_dir_exists():
    return config.APP_BASE_PATH.is_dir()

print(app_base_dir_exists())