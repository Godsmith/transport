"""Contains the Controller class."""
from transport.interfaces.model import Model
from transport.interfaces.view import View
from transport.model.path import Path, Point


class Controller:
    """The controller in MVC-like fashion."""

    def __init__(self, model: Model, view: View):
        self._model = model
        view.set_touch_down_callback(self.touch_down)
        view.set_touch_move_callback(self.touch_move)
        view.set_update_callback(self.update)
        self._view = view

    def run(self):
        """Start the view afte all callbacks have been set."""
        self._view.run()

    def touch_down(self, x_index, y_index):
        """Called when the user touches an index in the grid."""
        self._model.add_path(Path(Point(x_index, y_index)))

    def touch_move(self, x_index, y_index):
        """Called when the user drags from one index to another in the grid"""
        point = Point(x_index, y_index)
        if self._model.paths[-1][-1] != point:
            self._model.paths[-1].append(point)

    def update(self, dt: float):
        """Called each frame."""
        self._model.update(dt)
        self._view.update(self._model.paths, self._model.factories)
