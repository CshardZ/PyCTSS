from prompt_toolkit import prompt
from prompt_toolkit.document import Document



class File: # TODO to rename as CTSSFileSystem, that CRUD all file ops
    def __init__(self, path):
        self.file = path
        self.name = None
        self.size = None
        self.created = None
        self.updated = None
        self.existing_content = None
        self.new_content = None

    def open(self):
        self.existing_content = self.file.read_text()

    def view(self):
        doc = Document(text=self.existing_content)
        prompt("Read-only note (press Enter):\n", default=doc)

    def edit(self):
        self.new_content = prompt(
            "Edit your note (Press Esc + Enter to finish):\n",
            multiline=True,
            default=self.existing_content
        )

    def save(self):
        print("saving this: ",self.new_content)
        self.file.write_text(self.new_content)

    def write_binary(self, content):
        self.file.write_bytes(content)

    def read_binary(self):
        file_bytes = self.file.read_bytes()
        return file_bytes
    
    def write_text(self, content):
        self.file.write_text(content)

    def read_text(self):
        content = self.file.read_text()
        return content