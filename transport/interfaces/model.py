"""Contains the Model interface."""
from abc import ABC, abstractmethod
from typing import List

from transport.model.factory import Factory
from transport.model.path import Path


class Model(ABC):
    """Interface for Models in the MVC fashion for the game."""

    @property
    @abstractmethod
    def paths(self) -> List[Path]:
        """Return all paths in the model."""
        raise NotImplementedError

    @property
    @abstractmethod
    def factories(self) -> List[Factory]:
        """Return all factories in the model."""
        raise NotImplementedError

    @abstractmethod
    def add_path(self, path: Path):
        """Add a path to the model"""
        raise NotImplementedError

    def update(self, dt):
        """Tick forward a certain time."""
        for path in self.paths:
            path.update(dt)
        for factory in self.factories:
            factory.update(dt)
