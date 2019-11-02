"""Contains the Factory class."""
from typing import List

from transport.model.resource import Resource


class Factory:
    """A factory is a place that produces and/or consumes resources."""

    def __init__(
        self,
        x: int,
        y: int,
        creates: Resource = None,
        consumes: Resource = None,
        interval: float = 1.0,
        max_capacity: int = 1,
    ):
        self.x = x
        self.y = y
        self.creates = creates
        self.consumes = consumes
        self.interval = interval
        self.max_capacity = max_capacity
        self.time_to_next_production = self.interval
        self.resources: List[Resource] = []

    def update(self, dt):
        """Step forward in time."""
        if len(self.resources) < self.max_capacity:
            self.time_to_next_production -= dt
            if self.time_to_next_production <= 0:
                self.time_to_next_production += self.interval
                self.resources.append(self.creates)

    def pop(self):
        """Delete and return the latest resource produced."""
        return self.resources.pop()
