from openai import OpenAI
from pandas import DataFrame
from typing import List, Dict
from gptbatcher.Question import Question
from gptbatcher.Participant import Participant


class GPTBatcher:
    def __init__(self, api_key: str):
        self.openai = OpenAI(api_key=api_key)

    def ask(self, question: Question, participants: List[Participant]) -> DataFrame:
        pass

