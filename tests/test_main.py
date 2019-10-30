"""Test cases for the main.py module."""

# pylint: disable=protected-access

from kivy.graphics.instructions import Instruction

from transport.grid import Grid
from transport.main import GridWidget
from transport.path import Point, Path


def test_path_created_on_touch_down():
    """ Test that a touch in location A creates a Path starting and ending at A.
        -----------------
        |       |       |
        |   A   |       |
        |       |       |
        -----------------
        |       |       |
        |       |       |
        |       |       |
        -----------------
    """
    widget = GridWidget(Grid(2, 2))
    widget.on_touch_down(Point(widget.width * 1 / 4, widget.height * 3 / 4))
    assert widget.grid.paths == [Path(Point(0, 1))]


def test_path_created_on_touch_move():
    """ Test that a touch in location A and dragged to B creates a Path starting at A
        and ending at B.
        -----------------
        |       |       |
        |   B   |       |
        |       |       |
        -----------------
        |       |       |
        |   A   |       |
        |       |       |
        -----------------
    """
    widget = GridWidget(Grid(2, 2))
    widget.on_touch_down(Point(widget.width * 1 / 4, widget.height * 1 / 3))
    widget.on_touch_move(Point(widget.width * 1 / 4, widget.height * 3 / 4))

    expected = Path(Point(0, 0))
    expected.append(Point(0, 1))
    assert widget.grid.paths == [expected]


def test_update():
    """ Test just so that nothing crashes when calling the update method."""
    grid = Grid(2, 2)
    grid.add_path(Path(Point(0, 0)))
    widget = GridWidget(grid)
    widget.paths = Instruction()
    widget.update(0.1)


def test_repaint_gridlines():
    """ Test just so that nothing crashes."""
    widget = GridWidget(Grid(2, 2))
    widget.gridlines = Instruction()
    widget._repaint_gridlines(None, None)
