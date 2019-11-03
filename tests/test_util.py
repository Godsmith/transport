"""Test cases for the grid module."""

from transport.util import index_of_closest


def test_index_of_closest():
    """Given a value x and a list of values xs, return the index of the value in xs that
    is closest to x."""
    assert index_of_closest(3.2, [1, 2, 3, 4, 5]) == 2
