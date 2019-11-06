"""Test cases for the main.py module."""

# pylint: disable=protected-access

from kivy.graphics.instructions import InstructionGroup

from transport.controller import Controller
from transport.model.factory import Factory
from transport.view.app import TransportAppView
from transport.view.grid_widget import GridWidget
from transport.model.grid import Grid
from transport.model.path import Point, Path


class Touch:
    """Mock object simulating a touch event"""

    def __init__(self, x, y, button="left", is_double_tap=False):
        self.x = x
        self.y = y
        self.button = button
        self.is_double_tap = is_double_tap


def test_no_path_created_on_touch_down_and_then_up():
    """ Test that no path is created by just a single touch down without touch move"""
    grid = Grid(2, 2)
    widget = GridWidget(2)
    Controller(grid, TransportAppView(widget))

    touch = Touch(widget.width * 1 / 4, widget.height * 3 / 4)
    widget.on_touch_down(touch)
    widget.on_touch_up(touch)

    assert grid.paths == []


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

    widget.on_touch_down(Touch(widget.width * 1 / 4, widget.height * 1 / 3))
    widget.on_touch_move(Touch(widget.width * 1 / 4, widget.height * 3 / 4))
    widget.on_touch_up(Touch(widget.width * 1 / 4, widget.height * 3 / 4))

    expected = Path(Point(0, 0))
    expected.append(Point(0, 1))
    assert grid.paths == [expected]


def test_double_tap_to_remove_path():
    """ Test that a double tap in location A removes a Path in that location.
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

    widget.on_touch_down(Touch(widget.width * 1 / 4, widget.height * 1 / 3))
    widget.on_touch_move(Touch(widget.width * 1 / 4, widget.height * 3 / 4))
    widget.on_touch_up(Touch(widget.width * 1 / 4, widget.height * 3 / 4))

    widget.on_touch_down(
        Touch(widget.width * 1 / 4, widget.height * 1 / 3, is_double_tap=True)
    )
    widget.on_touch_up(Touch(widget.width * 1 / 4, widget.height * 1 / 3))

    assert grid.paths == []


def test_update():
    """ Test. just so that nothing crashes when calling the update method."""
    grid = Grid(2, 2)
    grid.add_path(Path(Point(0, 0)))
    grid.add(Factory(x=1, y=1))
    widget = GridWidget(2)
    widget.paths = [InstructionGroup()]
    widget.factories = [InstructionGroup()]
    controller = Controller(grid, TransportAppView(widget))

    controller.update(0.1)


# def test_repaint_gridlines():
#     """ Test just so that nothing crashes."""
#     widget = GridWidget(2)
#     widget.gridlines = InstructionGroup()
#     widget._repaint_gridlines(None, None)
