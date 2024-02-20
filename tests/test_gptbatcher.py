import json
from typing import Dict
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from gptbatcher import GPTBatcher, Question, Choice, Participant

import datetime
from unittest.mock import patch

from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function
from openai.types.chat.chat_completion import ChatCompletion, Choice as ChatCompletionChoice


def create_chat_completion(arguments: Dict[str, bool]) -> ChatCompletion:
    return ChatCompletion(
        id="foo",
        model="gpt-3.5-turbo",
        object="chat.completion",
        choices=[
            ChatCompletionChoice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    role="assistant",
                    tool_calls=[
                        ChatCompletionMessageToolCall(
                            id="foo",
                            type="function",
                            function=Function(
                                name="vote",
                                arguments=json.dumps(arguments),
                            )
                        )
                    ]
                ),
            )
        ],
        created=int(datetime.datetime.now().timestamp()),
    )

class TestGPTBatcher(TestCase):
    def setUp(self):
        self.api_key = 'test_key'
        self.rpm = 3
        self.model = 'gpt-3.5-turbo'
        self.temperature = 0.5

    @patch("openai.resources.chat.Completions.create")
    def test_ask(self, mock_create):
        mock_create.return_value = create_chat_completion({"Berlin": True, "Munich": False, "Hamburg": False, "Frankfurt": False})
        gpt_batcher = GPTBatcher(api_key=self.api_key, rpm=self.rpm, model=self.model, temperature=self.temperature)
        question = Question(
            label="Capital of Germany",
            prompt="What is the capital of Germany?",
            choices=[
                Choice(label="Berlin", prompt="Berlin"),
                Choice(label="Munich", prompt="Munich"),
                Choice(label="Hamburg", prompt="Hamburg"),
                Choice(label="Frankfurt", prompt="Frankfurt")
            ]
        )
        participant = Participant(label="Segment A", prompt="You are a 26 year old male from Birmingham, UK", weight=10)
        result = gpt_batcher.ask(question, [participant], 1)
        self.assertEqual(result.at[participant.label, "Berlin"], 1)

    @patch("openai.resources.chat.Completions.create")
    def test_failed_ask(self, mock_create):
        mock_create.return_value = create_chat_completion({"Berlin": False, "Munich": False, "Hamburg": False, "Frankfurt": False})
        gpt_batcher = GPTBatcher(api_key=self.api_key, rpm=self.rpm, model=self.model, temperature=self.temperature)
        question = Question(
            label="Capital of Germany",
            prompt="What is the capital of Germany?",
            choices=[
                Choice(label="Berlin", prompt="Berlin"),
                Choice(label="Munich", prompt="Munich"),
                Choice(label="Hamburg", prompt="Hamburg"),
                Choice(label="Frankfurt", prompt="Frankfurt")
            ]
        )
        participant = Participant(label="Segment A", prompt="You are a 26 year old male from Birmingham, UK", weight=10)
        with self.assertRaises(Exception):
            gpt_batcher.ask(question, [participant], 1)

    @patch("openai.resources.chat.Completions.create")
    def test_many_participants(self, mock_create):
        mock_create.return_value = create_chat_completion({"Berlin": True, "Munich": False, "Hamburg": False, "Frankfurt": False})
        gpt_batcher = GPTBatcher(api_key=self.api_key, rpm=self.rpm, model=self.model, temperature=self.temperature)
        question = Question(
            label="Capital of Germany",
            prompt="What is the capital of Germany?",
            choices=[
                Choice(label="Berlin", prompt="Berlin"),
                Choice(label="Munich", prompt="Munich"),
                Choice(label="Hamburg", prompt="Hamburg"),
                Choice(label="Frankfurt", prompt="Frankfurt")
            ]
        )
        participants = [
            Participant(label="Segment A", prompt="You are a 26 year old male from Birmingham, UK", weight=10),
            Participant(label="Segment B", prompt="You are a 45 year old female from London, UK", weight=10),
            Participant(label="Segment C", prompt="You are a 33 year old from Manchester, UK", weight=10),
        ]
        result = gpt_batcher.ask(question, participants, 3)
        self.assertEqual(result.sum()["Berlin"], 3)


if __name__ == '__main__':
    main()
