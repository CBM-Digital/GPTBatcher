from typing import List
from gptbatcher.Choice import Choice

class Question:
    def __init__(self, label: str, prompt: str, choices: List[Choice]):
        self.label = label
        self.prompt = prompt
        self.choices = choices

    def __str__(self):
        return self.label
    
    def __repr__(self):
        return self.label
    
    def __hash__(self):
        return hash(self.label)
    
    def __eq__(self, other):
        return self.label == other.label
    
    def __ne__(self, other):
        return self.label != other.label