import json
from openai import OpenAI
from pandas import DataFrame
from typing import List, Tuple
from gptbatcher.Question import Question
from gptbatcher.Participant import Participant
from gptbatcher.Choice import Choice
from gptbatcher.JobQueue import JobQueue

ParticipantChoice = Tuple[Participant, Choice]


async def ask_once(
    openai: OpenAI,
    model: str,
    temperature: float,
    question: Question,
    participant: Participant,
) -> ParticipantChoice:
    completion = openai.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": participant.prompt},
            {"role": "user", "content": question.prompt},
        ],
        tools=[
            {
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
                                    "description": choice.prompt,
                                }
                                for choice in question.choices
                            }
                        },
                        "required": [choice.label for choice in question.choices],
                    },
                },
            }
        ],
        tool_choice={"type": "function", "function": {"name": "vote"}},
    )

    choice = completion.choices[0]
    calls = choice.message.tool_calls
    if not calls or len(calls) != 1:
        raise Exception("Expected one tool call")

    json_string = calls[0].function.arguments
    results = json.loads(json_string)

    chosen = None
    for choice in question.choices:
        if choice.label in results and results[choice.label]:
            if chosen:
                raise Exception("Multiple choices selected")
            chosen = choice

    if not chosen:
        raise Exception("No choice selected")

    return (participant, chosen)


async def retry_ask_once(
    openai: OpenAI,
    model: str,
    temperature: float,
    question: Question,
    participant: Participant,
) -> ParticipantChoice:
    for _ in range(3):
        try:
            return await ask_once(openai, model, temperature, question, participant)
        except:
            pass
    raise Exception("Failed to vote")


class GPTBatcher:
    def __init__(
        self,
        api_key: str,
        rpm: int = 3,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.5,
    ):
        self.openai = OpenAI(api_key=api_key)
        self.rpm = rpm
        self.model = model
        self.temperature = temperature

    def ask(self, question: Question, participants: List[Participant]) -> DataFrame:
        jobs = []
        for participant in participants:
            for _ in range(participant.samples):
                jobs.append(
                    (
                        retry_ask_once,
                        (
                            self.openai,
                            self.model,
                            self.temperature,
                            question,
                            participant,
                        ),
                    )
                )
        job_queue = JobQueue(tokens=self.rpm, jobs=jobs)
        results: List[ParticipantChoice] = job_queue.run()
        df = DataFrame(
            0,
            columns=[choice.label for choice in question.choices],
            index=[participant.label for participant in participants],
        )
        for participant, choice in results:
            df.at[participant.label, choice.label] += 1
        return df
