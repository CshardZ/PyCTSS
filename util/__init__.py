from datetime import datetime


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