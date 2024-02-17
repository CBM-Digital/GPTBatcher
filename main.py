from gptbatcher import GPTBatcher, Question, Choice, Participant
import os

batcher = GPTBatcher(
    api_key=os.environ['OPENAI_API_KEY'],
    rpm=20, # 20 requests per minute
    model="gpt-3.5-turbo",
    temperature=1.5,
)

red = Choice(label="Red", prompt="Red")
green = Choice(label="Green", prompt="Green")
blue = Choice(label="Blue", prompt="Blue")
yellow = Choice(label="Yellow", prompt="Yellow")
other = Choice(label="Other", prompt="Other")


question = Question(
    label="Favourite Colour",
    prompt="What is your favourite colour?",
    choices=[red, green, blue, yellow, other]
)

segmentA = Participant(label="Newcastle Man", prompt="You are a 53 year old male from Newcastle, UK", samples=6)
segmentB = Participant(label="London Woman", prompt="You are a 26 year old female from London, UK", samples=6)

participants = [segmentA, segmentB]

result = batcher.ask(question=question, participants=participants)
print(question)
print(result)
# result = pd.DataFrame([[30, 20, 0, 0], [20, 30, 0, 0]], columns=['Berlin', 'Munich', 'Hamburg', 'Frankfurt'], index=['Segment A', 'Segment B'])


