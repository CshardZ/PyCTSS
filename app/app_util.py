from datetime import datetime
import itertools
from . import config


def create_base_dirs():
    dirs = [
        config.APP_BASE_PATH / config.ALL_USERS_PATH,
        config.APP_BASE_PATH / config.ALL_ADMINS_PATH,
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)


def get_files_info(path):
    files_info = {}
    for index, file in enumerate(path.iterdir(), start=1):
        stats = file.stat()
        files_info[index] = {
            'name': file.name,
            'size': str(stats.st_size),
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
        formatted_command = f"[[bold {color}]{command}[/bold {color}]]"
        formatted_option = f"[bold]{option}[/bold]"
        menu[formatted_command] = formatted_option
    return menu
    

def get_commands_for(options):
    return [option.upper() for option in options] #TODO adding only unique command, ex: Create, Cut would conflict!









