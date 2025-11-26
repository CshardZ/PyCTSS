import time
import random
import pathlib
import rich.console, rich.prompt
from . import app_util
from . import config
from . import file


class Interface:
    def __init__(self, user=None):
        self.screen = rich.console.Console()
        self.file: file.File
        self.user = user
        self.current_path = pathlib.Path("")
        if self.user:
            #TODO should change as user interacts with console
            self.current_path = pathlib.Path(str(config.USER_FILES_PATH).format(self.user.username))

    def clear_screen(self):
        self.screen.clear()

    def show_header(self):
        self.clear_screen()
        self.screen.rule(config.APP_NAME)
        self.screen.print(app_util.bread_crumbs_for(self.current_path))
        self.screen.rule()

    def show_splash_screen(self):
        def draw(progress): #TODO can move this to util or ... app_util?
            bar = ("░" * progress).ljust(100)
            self.clear_screen()
            self.screen.print("\n" * 10)
            self.screen.print(config.APP_LOGO, justify="center")
            self.screen.print(f"0 |{bar}| 100", justify="center")

        loading = 0
        steps = [10, 20, 30]
        while loading < 100:
            draw(loading)
            time.sleep(1)
            loading += random.choice(steps)

        draw(100)
        self.screen.print("\nPLEASE WAIT", justify="center")
        time.sleep(3)

    def show_menu(self, options):
        self.show_header()
        menu = app_util.build_menu_info(options)
        for command, option in menu.items():
            self.screen.print(command, option)
        self.screen.rule()

    def prompt_command(self, options):
        commands = app_util.get_commands_for(options)
        command = self.screen.input(config.PROMPT_STYLE).strip().upper()
        if command in commands:
            return command

    def prompt_login_credentials(self):
        self.show_header()
        username = rich.prompt.Prompt.ask("Username")
        password = rich.prompt.Prompt.ask("Password", password=True)
        return username, password #TODO Must return hashed password, build a custom hashing function with salting

    def show_files(self):
        self.show_header()
        files_table = app_util.build_rich_table(["File Number", "File Name", "Size", "Created", "Updated"])
        files_info = app_util.get_files_info(self.current_path)

        for index, details in files_info.items():
            index = f"{index:4d}"
            files_table.add_row(index,*details.values())
            
        self.screen.print(files_table, justify="center")


    def prompt_file_choice(self):
        file_number = int(self.screen.input("Enter File Number To Open: "))
        # TODO needs file number validation skipped for now
        files_info = app_util.get_files_info(self.current_path)
        if file_number in files_info:
            self.file = files_info[file_number]['name']
            self.screen.print(f"{files_info[file_number]['name']} Opened")


    def open_file_view(self):
        self.current_path = self.current_path / self.file
        self.show_header()
        self.file = file.File(self.current_path)
        self.file.open()
        self.file.edit()    

    def close_file_view(self):
        save = rich.prompt.Prompt.ask("Save file (y or n): ")
        if save == 'y':
            self.file.save()
            self.screen.print("File Saved")
        else:
            self.screen.print("File Not Saved")
        self.screen.print("Please wait...")
        time.sleep(3)
        self.clear_screen()
        #TODO move main view to self.current_path

class AdminInterface(Interface): #TODO email everytime admin logs in
    """
    Admin Tasks:
         - Create/Delete normal user
         - Create/Delete admin user
         - View Files(logs, user activities, sessions, tresspassing etc)
         - Server setting - don't know
    """
    
    def create_normal_user(self):
        pass

    def create_admin_user(self):
        pass
    
    def delete_normal_user(self):
        pass

    def delete_admin_user(self):
        pass

    def read_file(self):
        pass


class UserInterface(Interface):
    """
    User Tasks:
        - CRUD Personal Files
        - Share Files
        - Message other users
        - Report/Feedback/Contact to admins
    """

    def __init__(self, user):
        super().__init__(user)
        self.user = user



    def create_file(self):
        pass
    def edit_file(self):
        pass
    def delete_file(self):
        pass
    def send_message(self):
        pass
    def receive_message(self):
        pass
    def send_file(self):
        pass
    def receive_file(self):
        pass