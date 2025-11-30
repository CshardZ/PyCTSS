import time
import random
import pathlib
import rich.console, rich.prompt
from . import app_util
from . import config
from . import file
from auth import auth


class Interface:
    def __init__(self, client=None):
        self.screen = rich.console.Console()
        self.client = client

    def show_header(self):
        self.screen.clear()
        self.screen.rule(f"[bold]{config.APP_NAME}[/bold]")

    def load(self):
        print("load()")

    def show_splash_screen(self):
        self.screen.clear()
        time.sleep(3)
        self.screen.print("\n\n\n\n")
        self.screen.print(config.APP_LOGO, justify="center")
        time.sleep(2)
        app_util.show_progress_bar(self.screen)
        time.sleep(3)
        self.screen.print("\n[bold][blue]Welcome[/blue][/bold]", justify="center")
        time.sleep(2)
        self.screen.print("[bold][blue]to[/blue][/bold]", justify="center")
        time.sleep(1)
        self.screen.print("[bold][blue]PyCTSS[/blue][/bold]", justify="center")
        time.sleep(2)


    def choose_from_menu(self, options):
        self.screen.print()
        self.screen.rule(characters="-", style="grey")
        self.screen.print("[bold blue]Choose From Menu[/bold blue]")
        self.screen.rule(characters="-", style="grey")
        menu = app_util.build_menu_info(options)
        for command, option in menu.items():
            self.screen.print(command, option)
        self.screen.rule(style="grey")
        commands = app_util.get_commands_for(options)
        command = self.screen.input(config.PROMPT_STYLE).strip().upper()
        if command in commands:
            return commands[command]
        else:
            return ""

    def authenticate(self):
        self.show_header()
        username, verified, role = auth.CTSSAuth.sign_in(self.client)
        return username, verified, role

    def files_table(self, files_info):
        files_table = app_util.build_rich_table(["File Number", "File Name", "Size", "Created", "Updated"])
        for index, details in files_info.items():
            index = f"{int(index):4d}"
            files_table.add_row(index,*details.values())
        self.screen.print(files_table, justify="center")


    def choose_from_files(self):
        file_name = rich.prompt.Prompt.ask("Enter File Name with Extension")
        return file_name



class AdminInterface(Interface):

    def __init__(self, user, client):
        super().__init__()
        self.user = user
        self.current_path = config.CLIENT_SIDE_RELATIVE_ADMINS
        self.file: file.File
        self.client = client
    
    def start(self):
        self.client.connect_to_server() #NOTE can be done in init itself
        # while True:
        self.home()
        self.interact()

    def stop(self):
        pass
    
    def show_header(self):
        super().show_header()

    def home(self):
        self.show_header()

    def interact(self, options=None):
        if not options:
            options = [
                "Credentials-Registry",
                "Manage-Users",
            ]

        choice = self.choose_from_menu(options)
        self.current_path = self.current_path / choice

        if choice == "Credentials-Registry":
            self.file_explorer()
        elif choice == "Manage-Users":
            self.manage_users()

        self.current_path = self.current_path.parent

    def file_explorer(self):
        self.show_header()
        self.client.send("READ", "FOLDER", self.current_path)
        response = self.client.receive()
        super().open_file_explorer(dict(response))
        file_name = self.choose_from_files()
        self.client.send("READ", "FILE", (self.current_path / file_name))
        response = self.client.receive()
        (config.CLIENT_TEMP_FOLDER_PATH / "temp.txt").touch()
        self.file = file.File(config.CLIENT_TEMP_FOLDER_PATH / 'temp.txt')
        self.file.write_text(response)
        self.view_file()
        updated_text = self.file.read_text()
        self.client.send("UPDATE", "FILE", (self.current_path / file_name), updated_text)
        (config.CLIENT_TEMP_FOLDER_PATH / "temp.txt").unlink()

    def manage_users(self):
        options = [
            "Create User",
            "Delete User",
        ]
        choice = self.choose_from_menu(options)

        if choice == "Create User":
            self.create_user()
        elif choice == "Delete User":
            self.delete_user()

    def create_user(self):
        new_username = rich.prompt.Prompt.ask("New Username")
        new_password = rich.prompt.Prompt.ask("New Password", password=True)
        confirm_password = rich.prompt.Prompt.ask("Confirm Password", password=True)
        credentials = (new_username, new_password)
        self.client.send("CREATE", "USER", content=credentials)

    def delete_user(self):
        username = rich.prompt.Prompt.ask("Username to delete: ")
        credentials = (username, "")
        self.client.send("DELETE", "USER", content=credentials)
    
    def view_file(self):
        self.show_header()
        self.file.open()
        self.file.edit()  
        self.file.save()



class UserInterface(Interface):

    def __init__(self, user, client):
        super().__init__()
        self.user = user
        self.client = client
        self.user_path = pathlib.Path(str(config.CLIENT_SIDE_RELATIVE_USERS).format(self.user.username))
        self.current_path = self.user_path
        self.user_input = ""

    def start(self):
        self.client.connect_to_server()
        self.show_splash_screen()
        self.interact()

    def show_header(self):
        super().show_header()
        self.screen.print(f"[yellow]{app_util.bread_crumbs_for(self.current_path)}[/yellow]")
        self.screen.rule()
        self.screen.print()

    def interact(self):
        while True:
            self.home_view()
            self.folder_view()

    def home_view(self):
        self.show_header()
        self.user_input = self.choose_from_menu([
            "Files",
            "Shared",
            "Profile",
            "Setting"
        ])

    def folder_view(self):
        self.current_path = self.current_path / self.user_input
        while True:
            files_details = self.client.read_folder(self.current_path)
            self.show_header()
            self.files_table(files_details)
            self.user_input = self.choose_from_menu([
                "Create File",
                "Edit File",
                "Delete File",
                "Share File",
                "Go Back",
            ])

            if self.user_input == "Go Back":
                self.current_path = self.current_path.parent
                break

            self._handle_file_operation(self.user_input)


    def _handle_file_operation(self, user_input):
        file_name = rich.prompt.Prompt.ask("Enter file name")
        self.current_path = self.current_path / file_name
        self.show_header()
        
        if user_input == "Create File":
            self.client.create_file(self.current_path)
        elif user_input == "Edit File":
            temp_file = self.client.read_file(self.current_path)
            self.file = file.CTSSFileHandler(temp_file)
            self.file.open()
            self.file.edit()
            self.file.save()
            self.client.update_file(self.current_path, content = self.file.read_text())
        elif user_input == "Delete File":
            self.client.delete_file(self.current_path)
        elif user_input == "Share File":
            receiver = rich.prompt.Prompt.ask("Enter Receiver Username")
            self.client.share_file(self.current_path, receiver=receiver)
        
        self.current_path = self.current_path.parent