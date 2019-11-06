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
        view.set_touch_up_callback(self.touch_up)
        view.set_update_callback(self.update)
        view.set_double_tap_callback(self.double_tap)
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

    def touch_up(self) -> None:
        """Called when the user releases the touch."""
        if len(self._model.paths[-1]) <= 1:
            del self._model.paths[-1]

    def double_tap(self, x_index, y_index):
        """Called when the user double taps a cell"""
        path = next(
            (path for path in self._model.paths if Point(x_index, y_index) in path),
            None,
        )
        if path:
            self._model.paths.remove(path)

    def update(self, dt: float):
        """Called each frame."""
        self._model.update(dt)
        self._view.update(self._model.paths, self._model.factories)
