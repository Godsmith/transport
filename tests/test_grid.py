"""Test cases for the grid module."""

# pylint: disable=protected-access
from transport.main import GridWidget


def test_index_of_closest():
    """Given a value x and a list of values xs, return the index of the value in xs that
    is closest to x."""
    assert GridWidget._index_of_closest(3.2, [1, 2, 3, 4, 5]) == 2
