"""Module containing the Path class."""
from collections import namedtuple
from typing import Callable, List

from transport.model.resource import Resource

Point = namedtuple("Point", ("x", "y"))


class Path:
    """Represents a path which an agent travels on."""

    def __init__(self, point: Point, speed: float = 2):
        self.points: List[Point] = []
        self.points.append(point)
        self._square_index = 0
        self.direction = 1
        self.distance_to_next_square = 0.0
        self.speed = speed
        self.resources: List[Resource] = []
        self._end_of_line_callback = lambda x, y: None

    def __eq__(self, other):
        return self.points == other.points

    def __getitem__(self, item):
        return self.points[item]

    def __len__(self):
        return len(self.points)

    def append(self, point: Point):
        """Add a new point to the list"""
        self.points.append(point)

    def set_end_of_line_callback(self, method: Callable[["Path", Point], None]):
        """Set the method to be called when the agent reaches end of the line."""
        self._end_of_line_callback = method

    def update(self, dt):
        """Called for each game tick to update the agent location."""
        self.distance_to_next_square += dt * self.speed
        if self.distance_to_next_square >= 1.0:
            self.distance_to_next_square -= 1.0
            self._next_square()

    def _next_square(self):
        if len(self) > 1:
            self._square_index += self.direction
            if self._square_index == 0 or self._square_index == len(self) - 1:
                self._end_of_line_callback(self, self.point_agent_is_leaving)
                self.direction *= -1

    @property
    def point_agent_is_leaving(self) -> Point:
        """The last point the agent was visiting."""
        return self[self._square_index]

    @property
    def point_agent_is_approaching(self) -> Point:
        """The next point the agent will visit."""
        if len(self) == 1:
            return self[0]
        return self[self._square_index + self.direction]

    def pop(self) -> Resource:
        """Remove the resource that is currently carried and return it."""
