"""This module contains the Grid class."""
from transport.interfaces.model import Model
from transport.model.path import Path, Point


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

    def end_of_line(self, path: Path, point: Point):
        """This is called when a certain Path reaches end of the line at a certain
        Point"""

    def add_path(self, path: Path):
        """Add a path to the grid."""
        self._paths.append(path)
        path.set_end_of_line_callback(self.end_of_line)
