import json
from itertools import product

from gptbatcher import Participant

# Assuming the Participant class is defined elsewhere as provided

def load_data(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)["England"]

def generate_combinations(data):
    age_ranges = data["age_range"]
    education_levels = list(data["education"].keys())
    marital_statuses = [status["status"] for status in data["marital_status"]]
    races = list(data["race"].keys())
    genders = ["male", "female"]

    return product(age_ranges, genders, races, marital_statuses, education_levels)

def generate_participants(combinations):
    participants = []
    for age_range, gender, race, marital_status, education in combinations:
        age_min, age_max = age_range["range"]
        label = f"{gender.capitalize()}, {age_min}-{age_max}, {race}, {marital_status}, {education}"
        prompt = f"You are a {age_min}-{age_max} year old {gender} from England, UK, of {race} race, {marital_status}, with {education} education"
        # Simplify samples calculation; for demo purposes, we use a placeholder value
        samples = 1
        participants.append(Participant(label=label, prompt=prompt, samples=samples))

    return participants

# Path to the JSON file
file_path = 'england.json'

# Load data from JSON
data = load_data(file_path)

# Generate all possible combinations
combinations = generate_combinations(data)

# Generate participant instances
participants = generate_participants(combinations)

# For demonstration, print details of the first few participants
for participant in participants[:5]:
    print(f"Label: {participant.label}, Prompt: {participant.prompt}, Samples: {participant.samples}")
