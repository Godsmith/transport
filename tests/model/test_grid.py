"""Test cases for the Grid class."""
from transport.model.factory import Factory
from transport.model.grid import Grid
from transport.model.path import Path, Point
from transport.model.resource import Resource


def test_end_of_line_called(monkeypatch):
    """Test that the Path calls end_of_line when it comes to the end of the line."""

    class ArgCollector:
        """Class used for mocking that just collects the arguments from a method call"""

        def __init__(self):
            self.args = None

        def collect_args(self, *args):
            """Used for mocking a method call; collect the arguments for later use."""
            self.args = args

    collector = ArgCollector()
    monkeypatch.setattr(Grid, "end_of_line", collector.collect_args)

    factory = Factory(x=0, y=0, creates=Resource.BLUE, max_capacity=1)
    factory.resources = [Resource.BLUE]

    path = Path(Point(1, 1))
    path.append(Point(0, 1))

    grid = Grid(3, 3)
    grid.add(factory)
    grid.add_path(path)

    grid.update(1.1)

    assert collector.args == (path, Point(0, 1))


def test_agent_picks_up_resource():
    """Assert that when an agent reaches end of the line, it picks up a resource
    from an adjacent factory"""
    factory = Factory(x=0, y=0, max_capacity=1)
    factory.resources = [Resource.BLUE]

    path = Path(Point(1, 1))
    path.append(Point(0, 1))

    grid = Grid(3, 3)
    grid.add(factory)
    grid.add_path(path)

    grid.update(1.1)

    assert factory.resources == []
    assert path.resource == Resource.BLUE


def test_agent_continues_when_stopping_by_empty_factory():
    """If the station that the agent reverses by is empty, nothing shall happen"""
    factory = Factory(x=0, y=0, max_capacity=1)

    path = Path(Point(1, 1))
    path.append(Point(0, 1))

    grid = Grid(3, 3)
    grid.add(factory)
    grid.add_path(path)

    grid.update(1.1)

    assert factory.resources == []
    assert path.resource is None


def test_agent_reversing_adjacent_to_no_stations():
    """If the agent reverses next to no stations, it should keep its resources"""
    path = Path(Point(1, 1))
    path.append(Point(0, 1))
    path.resource = Resource.BLUE

    grid = Grid(3, 3)
    grid.add_path(path)

    grid.update(1.1)

    assert path.resource == Resource.BLUE
