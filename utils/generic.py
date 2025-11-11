import pathlib
from . import variables


# Main Functions
# =======================================================================================
def get_app_directory_path():
    return pathlib.Path.home() / variables.DESKTOP_DIR / variables.APP_DIR



def build_menu_info(menu_items):
    color_index = -1
    raw_menu = {}
    formated_menu = {}

    for item in menu_items:
        raw_menu[item[0].lower()] = item
        color = variables.RICH_COLORS[color_index]
        command_letter = f"[bold {color}]{item[0]}[/bold {color}]"
        with_brackets = f"[{command_letter}]"
        formated_menu[with_brackets] = f"[bold]{item}[/bold]"
        color_index -= 1

    print(formated_menu)
    print(raw_menu)
    return raw_menu, formated_menu


from rich.console import Console
Console().print('[[bold bright_cyan]C[/bold bright_cyan]]')
build_menu_info(["Create", 'DELETE', 'UPDATE'])