"""Contains the TransportAppView class. """
from typing import Iterable, List

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatterlayout import ScatterLayout
from kivy.config import Config

from transport.interfaces.view import View
from transport.model.factory import Factory
from transport.model.path import Path
from transport.view.grid_widget import GridWidget


class TransportAppView(View):
    """Concrete class implementing the View interface using Kivy."""

    def __init__(self, grid_widget: GridWidget):
        Config.read("config.ini")
        super(TransportAppView, self).__init__()
        self._update_callback = None
        self._grid_widget = grid_widget

    def run(self):
        _TransportApp(self._grid_widget).run()

    def update(self, paths: Iterable[Path], factories: List[Factory]):
        self._grid_widget.update(paths=paths, factories=factories)

    def set_update_callback(self, method):
        self._update_callback = method
        Clock.schedule_interval(self._update_callback, 1.0 / 60.0)

    def set_touch_down_callback(self, method):
        self._grid_widget.touch_down_callback = method

    def set_touch_move_callback(self, method):
        self._grid_widget.touch_move_callback = method

    def set_touch_up_callback(self, method):
        self._grid_widget.touch_up_callback = method

    def set_double_tap_callback(self, method):
        self._grid_widget.double_tap_callback = method


class _TransportApp(App):
    """The main app of the game."""

    def __init__(self, grid_widget: GridWidget):
        super(_TransportApp, self).__init__()
        self._update_callback = None
        self._grid_widget = grid_widget

    def build(self):  # pylint: disable=no-self-use; # pragma: no cover
        """Called when the app is created."""
        layout = ScatterLayout(
            translation_touches=2, do_rotation=False, scale_min=0.2, scale_max=1.5
        )
        layout.add_widget(self._grid_widget)
        return layout
