# GPTBatcher

GPTBatcher is a Python package that allows you to run multiple GPT-3 completions in parallel. It is useful for running surveys, polls, or any other task that requires multiple completions. It returns a pandas data frame with the results.

## Installation

```bash
pip install gptbatcher
```

## Usage

```python
from gptbatcher import GPTBatcher, Question, Choice, Participant
import os

batcher = GPTBatcher(api_key=os.environ['OPENAI_API_KEY'], rpm=20)

berlin = Choice(label="Berlin", prompt="Berlin")
munich = Choice(label="Munich", prompt="Munich")
hamburg = Choice(label="Hamburg", prompt="Hamburg")
frankfurt = Choice(label="Frankfurt", prompt="Frankfurt")

question = Question(
    label="Capital of Germany",
    prompt="What is the capital of Germany?",
    choices=[berlin, munich, hamburg, frankfurt]
)

segmentA = Participant(label="Segment A", prompt="You are a 26 year old male from Birmingham, UK", samples=10)
segmentB = Participant(label="Segment B", prompt="You are a 45 year old female from London, UK", samples=20)

participants = [segmentA, segmentB]

result = batcher.ask(question=question, participants=participants)
# result = pd.DataFrame([[10, 0, 0, 0], [20, 0, 0, 0]], columns=['Berlin', 'Munich', 'Hamburg', 'Frankfurt'], index=['Segment A', 'Segment B'])
print(question)
print(result.sum())
```

## Running the tests

```bash
python -m unittest discover
```

## Running the example

```bash
python3 -m examples.soothsayer
```

## Contributing

Please raise an issue if you find a bug or have a feature request. Pull requests are welcome.

## Support

CBM Digital offers support services for this package. Please contact us at https://www.cbmdigital.com/contact/, or by email at contact@cbmdigital.co.uk

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details