import json
from openai import OpenAI
from pandas import DataFrame
from typing import List, Dict
from gptbatcher.Question import Question
from gptbatcher.Participant import Participant
from gptbatcher.Choice import Choice


def ask_once(openai: OpenAI, question: Question, participant: Participant) -> Choice:
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": participant.prompt},
            {"role": "user", "content": question.prompt},
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "vote",
                "description": "Vote on a poll",
                "parameters": {
                    "type": "object",
                    "properties": {
                        **{
                            choice.label: {
                                "type": "boolean",
                                "description": choice.prompt
                            } for choice in question.choices
                        }
                    },
                    "required": [choice.label for choice in question.choices],
                }
            }
        }],
        tool_choice={
            "type": "function",
            "function": {
                "name": "vote",
            }
        }
    )

    choice = completion.choices[0]
    if choice.finish_reason is not "tool_calls":
        raise Exception("Tool call not made")
    
    calls = choice.message.tool_calls
    if not calls or len(calls) != 1:
        raise Exception("Expected one tool call")

    json_string = calls[0].function.arguments
    results = json.loads(json_string)

    chosen = None
    for choice in question.choices:
        if results[choice.label]:
            if chosen:
                raise Exception("Multiple choices selected")
            chosen = choice

    if not chosen:
        raise Exception("No choice selected")
    
    return chosen


class GPTBatcher:
    def __init__(self, api_key: str):
        self.openai = OpenAI(api_key=api_key)

    def ask(self, question: Question, participants: List[Participant]) -> DataFrame:
        raise NotImplementedError