"""This module contains the Grid class."""
from path import Path


class Grid:
    """The grid class is an abstract representation of the grid which all factories and
    paths are built on.

    A grid consists of width x height cells, and paths between those cells.

    The grid does not concern itself with the height or width in pixels."""

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.entities = {}
        self.paths = []

    def add(self, entity, position):
        """Add an entity to a specific position."""
        self.entities[position] = entity

    def add_path(self, path: Path):
        """Add a path to the grid."""
        self.paths.append(path)

    def update(self, dt):
        """Tick forward a certain time."""
        for path in self.paths:
            path.update(dt)
