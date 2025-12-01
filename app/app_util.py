import itertools
import rich
import time
import config
from rich.progress import Progress, BarColumn
from rich.align import Align
from rich.live import Live


def create_server_dirs():
    dirs = [
        config.ALL_USERS_PATH,
        config.ALL_ADMINS_PATH,
        config.ADMIN_PASSWORDS_PATH,
        config.USER_PASSWORDS_PATH
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)


def create_client_dirs():
    dirs = [
        config.CLIENT_WORKING_DIRECTORY_PATH
    ]
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)



def build_rich_table(cols):
    table = rich.table.Table()
    for col in cols:
        table.add_column(col)
    return table


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
    return {option[0].upper():option for option in options}

def bread_crumbs_for(path):
    parts = path.parts

    if "ADMINS" in parts:
        start = parts.index("ADMINS")
    elif "USERS" in parts:
        start = parts.index("USERS")
    else:
        start = 0

    return "lan.pyctss.app > " + " > ".join(parts[start:])


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