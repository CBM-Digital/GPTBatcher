class Choice:
    def __init__(self, label: str, prompt: str):
        self.label = label
        self.prompt = prompt

    def __str__(self):
        return self.label
