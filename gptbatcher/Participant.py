class Participant:
    def __init__(self, label: str, prompt: str, weight: float):
        self.label = label
        self.prompt = prompt
        self.weight = weight

    def __str__(self):
        return self.label
