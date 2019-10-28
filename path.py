from collections import namedtuple

Point = namedtuple("Point", ("x", "y"))


class Path(list):
    def __init__(self, point: Point):
        super(Path, self).__init__()
        self.append(point)
        self._square_index = 0
        self.direction = 1
        self.distance_to_next_square = 0.0

    def update(self, dt):
        self.distance_to_next_square += dt

    @property
    def point_agent_is_leaving(self) -> Point:
        return self[self._square_index]

    @property
    def point_agent_is_approaching(self) -> Point:
        if len(self) == 1:
            return self[0]
        else:
            return self[self._square_index + self.direction]
