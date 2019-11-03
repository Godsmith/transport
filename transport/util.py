"""Assorted utility methods used by multiple modules."""
from typing import Iterable


def index_of_closest(value: float, values: Iterable[float]):
    """Return the index of the value closest to <value> in <values>"""
    diffs = [abs(value - val) for val in values]
    return diffs.index(min(diffs))
