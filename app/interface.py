import pathlib
import rich.console
import prompt_toolkit
import util
from . import config




class Interface:

    RICH_PROMPT = "[bold blue3]Command: [/bold blue3]"
    HEADING = "| PyCTSS |"

    def __init__(self, user=None):
        self.screen = rich.console.Console()
        self.user = user
        self.file = None  # TODO: track current selected file

    def clear(self):
        self.screen.clear()

    def show_header(self):
        self.clear()
        self.screen.rule(self.HEADING)

    def show_menu(self, options):
        self.show_header()
        menu = util.build_menu_info(options)
        for command, option in menu.items():
            self.screen.print(command, option)
        self.screen.rule()

    def prompt_command(self, options):
        commands = util.get_commands_for(options)
        command = self.screen.input(self.RICH_PROMPT).strip().upper()

        if command in commands:
            return command



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







    Interface().show_menu(["Create", "Delete", "Update", "Read"])
    # Interface().prompt_choice({'c': 'Create', 'D': 'DELETE', 'U': 'UPDATE'})
    # interface = Interface()
    # interface.show_files()
    # interface.prompt_file_choice()
    # interface.open_file_view() # view and edit mode
    # interface.close_file_view() # update and save mode

    pass