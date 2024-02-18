from typing import List
from gptbatcher.Choice import Choice


class Question:
    def __init__(self, label: str, prompt: str, choices: List[Choice]):
        self.label = label
        self.prompt = prompt
        self.choices = choices

    def __str__(self):
        return self.label
