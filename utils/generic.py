from datetime import datetime


# Main Functions
# =======================================================================================

def get_menu_info(menu_items):
    color_index = -1
    raw_menu = {}
    formated_menu = {}

    for item in menu_items:
        raw_menu[item[0].lower()] = item
        color = config.RICH_COLORS[color_index]
        command_letter = f"[bold {color}]{item[0]}[/bold {color}]"
        with_brackets = f"[{command_letter}]"
        formated_menu[with_brackets] = f"[bold]{item}[/bold]"
        color_index -= 1

    return raw_menu, formated_menu

def get_files_info(path):
    files_info = {}
    for index, file in enumerate(path.iterdir(), start=1):
        stats = file.stat()
        files_info[index] = {
            'name': file.name,
            'size': str(stats.st_size),
            'created': datetime.fromtimestamp(stats.st_birthtime).strftime("%Y-%m-%d %H:%M:%S"),
            'updated': datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    return files_info