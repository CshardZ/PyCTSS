import pathlib
import rich
import prompt_toolkit
from rich.console import Console
import util
from app import config




class Interface:
    def __init__(self, user=None):
        self.screen = Console()
        self.user = user
        self.file = None # TODO need file object here, and to track current selected or opened file

    def clear(self):
        self.screen.clear()

    def show_header(self):
        self.clear()
        self.screen.rule("| PyCTSS |")

    def display_menu(self, menu_info: dict): # TODO Under maintenance
        self.show_header()
        for k, v in menu_info.items():
            self.screen.print(k,v)
        self.screen.rule()

    def prompt_choice(self, menu_info: dict): # TODO Under maintenance
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
        users_files_path = pathlib.Path(str(config.USER_PERSONAL_FILES_PATH).format(self.user))
        files_info = util.get_files_info(users_files_path)

        for index, file in files_info.items():
            table.add_row(f"{index:4d}",file['name'] ,file['size'], file['updated'], file['created'])
        self.screen.print(table, justify="center")



    def prompt_file_choice(self):
        file_number = int(self.screen.input("Enter File Number To Open: "))
        # TODO needs file number validation skipped for now
        self.user = "vivek" # TODO should be self.user.username
        users_files_path = pathlib.Path(str(config.USER_PERSONAL_FILES_PATH).format(self.user))
        files_info = util.get_files_info(users_files_path)
        if file_number in files_info.keys():
            self.screen.print(f"{files_info[file_number]['name']} Opened")
            self.file = files_info[file_number]['name'] # TODO actually a file object not a string like this
            return files_info[file_number]['name']

    def open_file_view(self):
        self.user = "vivek" # TODO should be self.user.username
        file = pathlib.Path(str(config.USER_PERSONAL_FILES_PATH).format(self.user)) / self.file
        existing_content = file.read_text()
        text = prompt_toolkit.prompt(
            "Edit your note (Press Esc + Enter to finish):\n",
            multiline=True,
            default=existing_content
        )
        print("You WROTE:", text)
        self.new_content = text
    
    def close_file_view(self):
        self.user = "vivek" # TODO should be self.user.username
        file = pathlib.Path(str(config.USER_PERSONAL_FILES_PATH).format(self.user)) / self.file
        file.write_text(self.new_content, encoding="utf-8")


if __name__ == '__main__':
    arg={'[[bold bright_cyan]C[/bold bright_cyan]]': '[bold]Create[/bold]', '[[bold bright_magenta]D[/bold bright_magenta]]': '[bold]DELETE[/bold]', '[[bold bright_blue]U[/bold bright_blue]]': '[bold]UPDATE[/bold]'}
    Interface().display_menu(arg)
    Interface().prompt_choice({'c': 'Create', 'D': 'DELETE', 'U': 'UPDATE'})
    interface = Interface()
    interface.show_files()
    interface.prompt_file_choice()
    interface.open_file_view() # view and edit mode
    interface.close_file_view() # update and save mode

    pass