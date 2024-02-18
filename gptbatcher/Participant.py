class Participant:
    def __init__(self, label: str, prompt: str, samples: int):
        self.label = label
        self.prompt = prompt
        self.samples = samples

    def __str__(self):
        return self.label
