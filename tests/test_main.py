"""Test cases for the main.py module."""

# pylint: disable=protected-access

from kivy.graphics.instructions import InstructionGroup

from transport.controller import Controller
from transport.model.factory import Factory
from transport.view.app import TransportAppView
from transport.view.grid_widget import GridWidget
from transport.model.grid import Grid
from transport.model.path import Point, Path


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
    grid = Grid(2, 2)
    widget = GridWidget(2)
    Controller(grid, TransportAppView(widget))

    widget.on_touch_down(Point(widget.width * 1 / 4, widget.height * 3 / 4))

    assert grid.paths == [Path(Point(0, 1))]


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
    grid = Grid(2, 2)
    widget = GridWidget(2)
    Controller(grid, TransportAppView(widget))

    widget.on_touch_down(Point(widget.width * 1 / 4, widget.height * 1 / 3))
    widget.on_touch_move(Point(widget.width * 1 / 4, widget.height * 3 / 4))

    expected = Path(Point(0, 0))
    expected.append(Point(0, 1))
    assert grid.paths == [expected]


def test_update():
    """ Test. just so that nothing crashes when calling the update method."""
    grid = Grid(2, 2)
    grid.add_path(Path(Point(0, 0)))
    grid.add(Factory(x=1, y=1))
    widget = GridWidget(2)
    widget.paths = InstructionGroup()
    widget.factories = [InstructionGroup()]
    controller = Controller(grid, TransportAppView(widget))

    controller.update(0.1)


def test_repaint_gridlines():
    """ Test just so that nothing crashes."""
    widget = GridWidget(2)
    widget.gridlines = InstructionGroup()
    widget._repaint_gridlines(None, None)
