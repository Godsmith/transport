"""Contains the Factory class."""
from resource import Resource


class Factory:
    """A factory is a place that produces and/or consumes resources."""

    def __init__(self, creates: Resource = None, consumes: Resource = None):
        self.creates = creates
        self.consumes = consumes
