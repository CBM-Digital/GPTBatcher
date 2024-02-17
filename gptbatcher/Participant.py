class Participant:
    def __init__(self, label: str, prompt: str, samples: int):
        self.label = label
        self.prompt = prompt
        self.samples = samples

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label