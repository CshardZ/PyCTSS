import prompt_toolkit


class File:
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

    def edit(self):
        self.new_content = prompt_toolkit.prompt(
            "Edit your note (Press Esc + Enter to finish):\n",
            multiline=True,
            default=self.existing_content
        )

    def save(self):
        self.file.write_text(self.new_content)