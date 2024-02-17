from gptbatcher import GPTBatcher, Question, Choice, Participant
import os

batcher = GPTBatcher(api_key=os.environ['OPENAI_API_KEY'], rpm=3)

berlin = Choice(label="Berlin", prompt="Berlin")
munich = Choice(label="Munich", prompt="Munich")
hamburg = Choice(label="Hamburg", prompt="Hamburg")
frankfurt = Choice(label="Frankfurt", prompt="Frankfurt")

question = Question(
    label="Capital of Germany",
    prompt="What is the capital of Germany?",
    choices=[berlin, munich, hamburg, frankfurt]
)

segmentA = Participant(label="Segment A", prompt="You are a 26 year old male from Birmingham, UK", samples=50)
segmentB = Participant(label="Segment B", prompt="You are a 45 year old female from London, UK", samples=50)

participants = [segmentA, segmentB]

result = batcher.ask(question=question, participants=participants)
# result = pd.DataFrame([[30, 20, 0, 0], [20, 30, 0, 0]], columns=['Berlin', 'Munich', 'Hamburg', 'Frankfurt'], index=['Segment A', 'Segment B'])


