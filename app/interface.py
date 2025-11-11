from rich.console import Console


class Interface:
    def __init__(self):
        self.screen = Console()

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
        pass

    def get_file_choice(self):
        pass

    def open_file_view(self):
        pass
    
    def close_file_view(self):
        pass


if __name__ == '__main__':
    arg={'[[bold bright_cyan]C[/bold bright_cyan]]': '[bold]Create[/bold]', '[[bold bright_magenta]D[/bold bright_magenta]]': '[bold]DELETE[/bold]', '[[bold bright_blue]U[/bold bright_blue]]': '[bold]UPDATE[/bold]'}
    Interface().display_menu(arg)
    Interface().prompt_choice({'c': 'Create', 'D': 'DELETE', 'U': 'UPDATE'})

    pass