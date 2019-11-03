"""Module containing the Path class."""
from collections import namedtuple
from typing import Callable, Optional

from transport.model.resource import Resource

Point = namedtuple("Point", ("x", "y"))


class Path(list):
    """Represents a path which an agent travels on."""

    def __init__(self, point: Point, speed: float = 2):
        super(Path, self).__init__()
        self.append(point)
        self._square_index = 0
        self.direction = 1
        self.distance_to_next_square = 0.0
        self.speed = speed
        self.resource: Optional[Resource] = None
        self._end_of_line_callback = lambda x, y: None

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
