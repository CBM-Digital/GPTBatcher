from typing import Any, Callable, List, TypeVar, Union
import random


class Sampler:
    def __init__(
        self, items: List[Any], weight_function: Callable[[Any], Union[int, float]]
    ):
        self.items = items
        self.weight_function = weight_function

    def sample(self) -> Any:
        total_weight = sum(self.weight_function(item) for item in self.items)
        random_weight_point = random.uniform(0, total_weight)
        current_weight = 0
        for item in self.items:
            current_weight += self.weight_function(item)
            if current_weight > random_weight_point:
                return item
