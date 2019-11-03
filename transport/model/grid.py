"""This module contains the Grid class."""
from transport.interfaces.model import Model
from transport.model.path import Path


class Grid(Model):
    """The grid class is an abstract representation of the grid which all factories and
    paths are built on.

    A grid consists of width x height cells, and paths between those cells.

    The grid does not concern itself with the height or width in pixels."""

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self._factories = []
        self._paths = []

    @property
    def paths(self):
        return self._paths

    @property
    def factories(self):
        return self._factories

    def add(self, factory):
        """Add a factory to a specific position."""
        self._factories.append(factory)

    def add_path(self, path: Path):
        """Add a path to the grid."""
        self._paths.append(path)
