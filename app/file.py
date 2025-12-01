from prompt_toolkit import prompt
from prompt_toolkit.document import Document


class CTSSFileHandler:
    def __init__(self, path):
        self.file = path
        self.existing_content = None
        self.new_content = None

    def open(self):
        if not self.file.is_file():
            self.file.touch()
        self.existing_content = self.file.read_text()

    def view(self):
        doc = Document(text=self.existing_content)
        prompt("Read-only note (press Enter):\n", default=doc) # TODO not waiting for prompt

    def display(self):
        print(self.existing_content)

    def edit(self):
        self.new_content = prompt(
            "Edit your note (Press Esc + Enter to finish):\n",
            multiline=True,
            default=self.existing_content
        )

    def save(self):
        self.write_text(self.new_content)

    def write_text(self, content):
        self.file.write_text(content)

    def read_text(self):
        content = self.file.read_text()
        return content