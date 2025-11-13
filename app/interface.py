from rich.console import Console
import rich
from . import config
import pathlib
from datetime import datetime


class Interface:
    def __init__(self, user=None):
        self.screen = Console()
        self.user = user

    def clear(self):
        self.screen.clear()

    def show_header(self):
        self.clear()
        self.screen.rule("| PyCTSS |")

    def display_menu(self, menu_info: dict):
        self.show_header()
        for k, v in menu_info.items():
            self.screen.print(k,v)

    def prompt_choice(self, menu_info):
        choice = self.screen.input("[bold blue3]Command: [/bold blue3]")
        if choice.lower() in menu_info.keys():
            print("ok")
        else:
            print("invalid choice")

    def show_files(self):
        self.show_header()
        table = rich.table.Table()

        table.add_column("File Number", justify="right", style="cyan", no_wrap=True)
        table.add_column("File Name", style="magenta")
        table.add_column("Size", justify="right", style="green")
        table.add_column("Updated", justify="right", style="green")
        table.add_column("Created", justify="right", style="green")

        self.user = "vivek" # TODO should be self.user.username
        for idx, file in enumerate(pathlib.Path(str(config.USER_PERSONAL_FILES_PATH).format(self.user)).iterdir()):
            modified_time = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            created_time = datetime.fromtimestamp(file.stat().st_birthtime).strftime("%Y-%m-%d %H:%M:%S")
            table.add_row(f"{idx:4d}", str(file.name) , str(file.stat().st_size), modified_time, created_time)
        self.screen.print(table, justify="center")



    def prompt_file_choice(self):
        pass

    def open_file_view(self):
        pass
    
    def close_file_view(self):
        pass


if __name__ == '__main__':
    # arg={'[[bold bright_cyan]C[/bold bright_cyan]]': '[bold]Create[/bold]', '[[bold bright_magenta]D[/bold bright_magenta]]': '[bold]DELETE[/bold]', '[[bold bright_blue]U[/bold bright_blue]]': '[bold]UPDATE[/bold]'}
    # Interface().display_menu(arg)
    # Interface().prompt_choice({'c': 'Create', 'D': 'DELETE', 'U': 'UPDATE'})
    Interface().show_files()

    pass