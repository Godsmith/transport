""" Contains the View interface """
from abc import ABC, abstractmethod
from typing import Iterable, Callable, List

from transport.model.factory import Factory
from transport.model.path import Path


class View(ABC):
    """View interface in an MVC-like fashion"""

    @abstractmethod
    def run(self):
        """Start the view."""
        raise NotImplementedError

    @abstractmethod
    def update(self, paths: Iterable[Path], factories: List[Factory]):
        """Update the view with new data. Typically called every frame."""
        raise NotImplementedError

    @abstractmethod
    def set_update_callback(self, method: Callable[[float], None]):
        """Set the method that is called when the update event happens."""
        raise NotImplementedError

    @abstractmethod
    def set_touch_down_callback(self, method: Callable[[int, int], None]):
        """Set the method that is called when the touch down event happens"""
        raise NotImplementedError

    @abstractmethod
    def set_touch_move_callback(self, method: Callable[[int, int], None]):
        """Set the method that is called when the touch move event happens"""
        raise NotImplementedError

    @abstractmethod
    def set_touch_up_callback(self, method: Callable[[], None]):
        """Set the method that is called when the touch up event happens"""
        raise NotImplementedError
