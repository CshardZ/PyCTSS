import time
import random
import pathlib
import rich.console, rich.prompt
from . import app_util
from . import config
from . import file


class Interface:
    def __init__(self):
        self.screen = rich.console.Console()
        self.file: file.File


    def show_header(self):
        self.screen.clear()
        self.screen.rule(f"[bold]{config.APP_NAME}[/bold]")

    def load(self):
        print("load()")

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

    def choose_from_menu(self, options):
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

    def prompt_login_credentials(self):
        self.show_header()
        username = rich.prompt.Prompt.ask("Username")
        password = rich.prompt.Prompt.ask("Password", password=True)
        return username, password #TODO Must return hashed password, build a custom hashing function with salting

    def open_file_explorer(self, files_info):
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
    """
    User Can:
        - Create File
        - Delete File
        - Edit File
        - Share File
        - Message other users
    """

    def __init__(self, user, client):
        super().__init__()
        self.user = user
        self.current_path = pathlib.Path(str(config.CLIENT_SIDE_RELATIVE_USERS).format(self.user.username))
        self.client = client
        self.file: file.File

    def start(self):
        self.client.connect_to_server() #NOTE can be done in init itself
        # while True:
        self.home()
        self.interact()

    def stop(self):
        pass

    def show_header(self):
        return super().show_header()

    def home(self):
        self.show_header()


    def interact(self, options=None):
        options = [
            "Files",
            "Shared",
            "Contact",
            "Profile",
        ]
        choice = self.choose_from_menu(options)

        if not choice is None:
            self.current_path = self.current_path / choice

        if choice == "Files":
            self.file_explorer()

        self.current_path = self.current_path.parent

    def file_explorer(self):
        self.show_header()
        self.client.send("READ", "FOLDER", self.current_path)
        response = self.client.receive()
        super().open_file_explorer(dict(response))
        choice = self.choose_from_menu([
            "Create File",
            "Edit File",
            "Delete File",
            "Share File",
        ]).lower()

        if choice == 'create file':
            file_name = rich.prompt.Prompt.ask("Enter Filename With Extensoin: ")
            file_name = '_'.join(file_name.split(' '))
            self.client.send("CREATE", "FILE", self.current_path, content=file_name)
            print("check if created")

        elif choice == 'edit file':
            file_name = self.choose_from_files()
            self.client.send("READ", "FILE", (self.current_path / file_name))
            print("READ FILE path:", (self.current_path / file_name))
            response = self.client.receive()
            time.sleep(5)
            (config.CLIENT_TEMP_FOLDER_PATH / "temp.txt").touch()
            self.file = file.File(config.CLIENT_TEMP_FOLDER_PATH / 'temp.txt')
            self.file.write_text(response)
            self.edit_file()
            updated_text = self.file.read_text()
            print("UPDATE FILE path:", (self.current_path / file_name))
            self.client.send("UPDATE", "FILE", (self.current_path / file_name), updated_text)
            (config.CLIENT_TEMP_FOLDER_PATH / "temp.txt").unlink()

        elif choice == 'delete file':
            file_name = rich.prompt.Prompt.ask("Enter Filename With Extensoin: ")
            file_name = '_'.join(file_name.split(' '))
            self.client.send("DELETE", "FILE", self.current_path, content=file_name)
            print("check if deleted")

        elif choice == 'share file':
            file_name = rich.prompt.Prompt.ask("Enter Filename With Extensoin: ")
            receiver_username = rich.prompt.Prompt.ask("Enter receiver username: ")
            file_name = '_'.join(file_name.split(' '))
            receiver_path = pathlib.Path(str(config.CLIENT_SIDE_RELATIVE_USERS).format(receiver_username))
            self.client.send("SHARE", "FILE", (str(self.current_path),str(receiver_path / "Files")), content=(receiver_username, file_name))



    def edit_file(self):
        self.show_header()
        self.file.open()
        self.file.edit()  
        self.file.save()   

        save = rich.prompt.Prompt.ask("Save file (y or n): ")
        if save == 'y':
            self.file.save()
            self.screen.print("File Saved")
        else:
            self.screen.print("File Not Saved")
        self.screen.print("Please wait...")
        time.sleep(3)

    def delete_file(self):# TODO check for non-existing file
        file_name = rich.prompt.Prompt.ask("Enter Filename With Extensoin: ")
        file_name = '_'.join(file_name.split(' '))
        (self.current_path / file_name).unlink()

    def send_message(self):
        pass
    def receive_message(self):
        pass
    def send_file(self):
        pass
    def receive_file(self):
        pass
