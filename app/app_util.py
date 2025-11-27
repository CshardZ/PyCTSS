from datetime import datetime
import itertools
from . import config
import rich


def create_base_dirs():
    dirs = [
        config.APP_BASE_PATH / config.ALL_USERS_PATH,
        config.APP_BASE_PATH / config.ALL_ADMINS_PATH,
        config.ADMIN_CREDENTIALS_REGISTRY_PATH,
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)


def create_user(username, password):
    dirs = [
        config.ALL_USERS_PATH / username / "Files",
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)

    password_file = config.ADMIN_CREDENTIALS_REGISTRY_PATH / "temp.txt"
    password_file.touch()
    with open(password_file, 'a') as f:
        credential = f"{username}={password}\n"
        f.write(credential)

def delete_user(username):
    import shutil
    shutil.rmtree(config.ALL_USERS_PATH / username)

    password_file = config.ADMIN_CREDENTIALS_REGISTRY_PATH / "temp.txt"
    # read all lines
    with open(password_file, 'r') as f:
        lines = f.readlines()

    # write back only the lines that do NOT match the username
    with open(password_file, 'w') as f:
        for line in lines:
            if not line.startswith(username + "="):
                f.write(line)

def build_rich_table(cols): #TODO need colors to columns
    table = rich.table.Table()
    for col in cols:
        table.add_column(col)
    return table

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


def build_menu_info(options):
    color_cycle = itertools.cycle(config.RICH_STANDARD_COLORS)
    menu = {}
    for option in options:
        command = option[0].upper()
        color = next(color_cycle)
        formatted_command = f"[bold {color}]{command}[/bold {color}] -"
        formatted_option = f"{option}"
        menu[formatted_command] = formatted_option
    return menu
    

def get_commands_for(options):
    return {option[0].upper():option for option in options} #TODO adding only unique command, ex: Create, Cut would conflict!


def bread_crumbs_for(path):
    parts = path.parts

    if "ADMINS" in parts:
        start = parts.index("ADMINS")
    elif "USERS" in parts:
        start = parts.index("USERS")
    else:
        start = 0

    return "lan.pyctss.app > " + " > ".join(parts[start:])








