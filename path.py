from collections import namedtuple

Point = namedtuple("Point", ("x", "y"))


class Path(list):
    def __init__(self, point: Point, speed=2):
        super(Path, self).__init__()
        self.append(point)
        self._square_index = 0
        self.direction = 1
        self.distance_to_next_square = 0.0
        self.speed = speed

    def update(self, dt):
        self.distance_to_next_square += dt * self.speed
        if self.distance_to_next_square >= 1.0:
            self.distance_to_next_square -= 1.0
            self._next_square()

    def _next_square(self):
        if len(self) > 0:
            self._square_index += self.direction
            if self._square_index == 0 or self._square_index == len(self) - 1:
                self.direction *= -1

    @property
    def point_agent_is_leaving(self) -> Point:
        return self[self._square_index]

    @property
    def point_agent_is_approaching(self) -> Point:
        if len(self) == 1:
            return self[0]
        else:
            return self[self._square_index + self.direction]
