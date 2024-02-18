import os
from typing import Dict, List, Tuple, Union
import json
from itertools import product

from gptbatcher import Choice, GPTBatcher, Participant, Question

Combination = Tuple[Tuple[int, int], str, str, str, str]

WeightedCombinations = Dict[Combination, float]

def calculate_weight(data, combination: Combination) -> float:
    age_range, gender, race, marital_status, education = combination

    age_item = next(item for item in data["age_range"] if tuple(item["range"]) == age_range)
    age_weight = age_item["weight"] * age_item["gender_weights"][gender]
    race_weight = data["race"][race]
    marital_item = next(item for item in data["marital_status"] if item["status"] == marital_status)
    marital_weight = marital_item["weights"][gender]
    education_weight = data["education"][education]

    return age_weight * race_weight * marital_weight * education_weight

def generate_combinations(data) -> WeightedCombinations:
    age_ranges = [tuple(item["range"]) for item in data["age_range"]]
    education_levels = list(data["education"].keys())
    marital_statuses = [item["status"] for item in data["marital_status"]]
    races = data["race"].keys()
    genders = ["male", "female"]

    combinations = product(age_ranges, genders, races, marital_statuses, education_levels)

    weights = {}
    for age_range, gender, race, marital_status, education in combinations:
        weight = calculate_weight(data, (age_range, gender, race, marital_status, education))
        weights[(age_range, gender, race, marital_status, education)] = weight

    return weights

def generate_participants(combinations: WeightedCombinations, total_samples: int) -> List[Participant]:
    participants = []
    for (age_range, gender, race, marital_status, education), weight in combinations.items():
        age_min, age_max = age_range
        label = f"{gender.capitalize()}, {age_min}-{age_max}, {race}, {marital_status}, {education}"
        prompt = f"You are a {age_min}-{age_max} year old {gender} from England, UK, of {race} race, {marital_status}, with {education} education"
        samples = int(weight * total_samples)
        participants.append(Participant(label=label, prompt=prompt, samples=samples))

    return participants

def main():
    filepath = "england.json"
    with open(filepath, 'r') as file:
        data = json.load(file)
    data = data['England']

    combinations = generate_combinations(data)
    print("Total weight:", sum(combinations.values()))

    total_samples = 200
    print("Ideal total samples:", total_samples)
    participants = generate_participants(combinations, total_samples=total_samples)
    print("Real total samples:", sum(participant.samples for participant in participants))

    batcher = GPTBatcher(
        api_key=os.environ['OPENAI_API_KEY'],
        rpm=30, # 20 requests per minute
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

    result = batcher.ask(question=question, participants=participants)

    print(question)
    print(result)

if __name__ == "__main__":
    main()