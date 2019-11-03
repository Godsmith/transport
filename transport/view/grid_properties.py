"""Contains the GridProperties class."""
from typing import Tuple

from transport.model.path import Point
from transport.util import index_of_closest


class GridProperties:
    """A collection of methods for calculating coordinates and indexes on a grid
    with a certain width and height."""

    def __init__(self, width: float, height: float, rows: int):
        self.width = width
        self.height = height
        self.rows = rows

    def position_partway_between_two_cells(
        self, point1: Point, point2: Point, fraction: float
    ):
        """Find a position partway between two cells. """
        x1, y1 = self.to_pixels(*point1)
        x2, y2 = self.to_pixels(*point2)
        return x1 + (x2 - x1) * fraction, y1 + (y2 - y1) * fraction

    @property
    def cell_width(self) -> float:
        """The width of a single cell in the grid, in pixels."""
        return self.width / self.rows

    @property
    def cell_height(self) -> float:
        """The height of a single cell in the grid, in pixels."""
        return self.height / self.rows

    @property
    def _cell_x_centers(self):
        for i in range(0, self.rows + 1):
            yield self.cell_width * (i + 0.5)

    @property
    def _cell_y_centers(self):
        for i in range(0, self.rows + 1):
            yield self.cell_height * (i + 0.5)

    def to_pixels(self, x_index: int, y_index: int) -> Tuple[float, float]:
        """Convert a certain x and y index to the corresponding location in pixels."""
        return list(self._cell_x_centers)[x_index], list(self._cell_y_centers)[y_index]

    def closest_indices(self, x: float, y: float) -> Tuple[int, int]:
        """Return the x and y indices closest to the provided position."""
        x_index = index_of_closest(x, self._cell_x_centers)
        y_index = index_of_closest(y, self._cell_y_centers)
        return x_index, y_index
