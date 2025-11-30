from datetime import datetime
import itertools
from . import config
import rich
from rich.progress import Progress
import time


def create_base_dirs(): # NOTE server only
    dirs = [
        config.APP_BASE_PATH / config.ALL_USERS_PATH,
        config.APP_BASE_PATH / config.ALL_ADMINS_PATH,
        config.ADMIN_CREDENTIALS_REGISTRY_PATH,
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)


def create_client_dirs(): # NOTE client only, basically a cache area
    # only for client side temp storage, since server is the central storage
    config.CLIENT_TEMP_FOLDER_PATH.mkdir(parents=True, exist_ok=True)



def build_rich_table(cols): #TODO need colors to columns
    table = rich.table.Table()
    for col in cols:
        table.add_column(col)
    return table

def get_files_info(path): #TODO MOVED TO server_util.py
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


def show_progress_bar():
    with Progress() as progress:
        task = progress.add_task("Working...", total=100)

        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(0.02)

import time
from rich.console import Console
from rich.progress import Progress, BarColumn
from rich.align import Align
from rich.live import Live

def show_progress_bar(console):
    progress = Progress(
        BarColumn(),
        expand=False
    )
    task = progress.add_task("", total=100)
    with Live(Align.center(progress), console=console, refresh_per_second=10):
        for _ in range(100):
            progress.update(task, advance=1)
            time.sleep(0.05)

