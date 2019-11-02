"""Contains the Model interface."""
from abc import ABC, abstractmethod
from typing import Dict, List

from transport.model.factory import Factory
from transport.model.path import Path, Point


class Model(ABC):
    """Interface for Models in the MVC fashion for the game."""

    @property
    @abstractmethod
    def paths(self) -> List[Path]:
        """Return all paths in the model."""
        raise NotImplementedError

    @property
    @abstractmethod
    def factories(self) -> Dict[Point, Factory]:
        """Return all factories in the model."""
        raise NotImplementedError

    @abstractmethod
    def add_path(self, path: Path):
        """Add a path to the model"""
        raise NotImplementedError

    @abstractmethod
    def update(self, dt):
        """Go to the next time step."""
        raise NotImplementedError
