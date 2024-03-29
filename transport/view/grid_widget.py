"""Contains the GridWidget class"""
from typing import Iterable, List, Tuple

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.transformation import Matrix
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget

from transport.model.factory import Factory
from transport.model.path import Path
from transport.view.factory import FactoryView
from transport.view.grid_properties import GridProperties
from transport.view.path import PathView


class GridWidget(Widget):
    """The main grid of the game."""

    def __init__(self, rows: int):
        super(GridWidget, self).__init__()
        self.rows = rows
        self.grid_properties = GridProperties(self.width, self.height, self.rows)
        self.bind(size=self._resize)
        self.gridlines = InstructionGroup()
        self.paths: List[InstructionGroup] = []
        self.factories: List[InstructionGroup] = []
        self.touch_down_callback = lambda x_index, y_index: None
        self.touch_move_callback = lambda x_index, y_index: None
        self.touch_up_callback = lambda: None
        self.double_tap_callback = lambda x_index, y_index: None

    def update(self, paths: Iterable[Path], factories: List[Factory]):
        """Update all contents to the next frame"""
        self._paint_paths(paths)
        self._paint_factories(factories)

    def _resize(self, instance, value):  # pylint: disable=unused-argument
        self.grid_properties = GridProperties(self.width, self.height, self.rows)
        self._paint_gridlines()

    def _paint_gridlines(self):
        if self.gridlines:
            self.canvas.remove(self.gridlines)
        self.gridlines = InstructionGroup()
        self.gridlines.add(Color(1, 1, 1))
        for line in range(0, self.rows + 1):
            x = self.grid_properties.cell_width * line
            y = self.grid_properties.cell_height * line
            self.gridlines.add(Line(points=((x, 0), (x, self.height))))
            self.gridlines.add(Line(points=((0, y), (self.width, y))))
        self.canvas.add(self.gridlines)

    def _paint_paths(self, grid_paths: Iterable[Path]):
        for instruction_group in self.paths:
            self.canvas.remove(instruction_group)
        self.paths = []

        for grid_path in grid_paths:
            self.paths.extend(
                PathView(grid_path, self.grid_properties).instruction_groups
            )
        for instruction_group in self.paths:
            self.canvas.add(instruction_group)

    def _paint_factories(self, factories: List[Factory]):
        for instruction_group in self.factories:
            self.canvas.remove(instruction_group)
        self.factories = []

        for factory in factories:
            self.factories.extend(
                FactoryView(factory, self.grid_properties).instruction_groups
            )

        for instruction_group in self.factories:
            self.canvas.add(instruction_group)

    def on_touch_down(self, touch):
        """Called when someone clicks or touches the widget."""
        scroll_step = 1.1
        zoom_in = [scroll_step] * 3
        zoom_out = [1 / scroll_step] * 3
        if touch.button == "left":
            x, y = self.grid_properties.closest_indices(touch.x, touch.y)
            self.touch_down_callback(x, y)
            if touch.is_double_tap:
                self.double_tap_callback(x, y)
        elif touch.button == "right":
            touch.ud["last_touch_pos"] = self._touch_position_relative_to_window(touch)
        elif (
            touch.button == "scrolldown"
            and self.parent.parent.scale < self.parent.parent.scale_max
        ):
            self.parent.parent.apply_transform(
                Matrix().scale(*zoom_in),
                anchor=self._touch_position_relative_to_window(touch),
            )
        elif (
            touch.button == "scrollup"
            and self.parent.parent.scale > self.parent.parent.scale_min
        ):
            self.parent.parent.apply_transform(
                Matrix().scale(*zoom_out),
                anchor=self._touch_position_relative_to_window(touch),
            )

    def _touch_position_relative_to_window(self, touch) -> Tuple[float, float]:
        return self.parent.parent.to_parent(*touch.pos)

    def on_touch_move(self, touch):
        """Called when, after a touch down, someone drags inside the widget."""
        if touch.button == "left":
            x, y = self.grid_properties.closest_indices(touch.x, touch.y)
            self.touch_move_callback(x, y)
        elif touch.button == "right":
            if "last_touch_pos" in touch.ud:
                x, y = self._touch_position_relative_to_window(touch)
                last_touch_x, last_touch_y = touch.ud["last_touch_pos"]
                touch.ud["last_touch_pos"] = (x, y)
                translation = (x - last_touch_x, y - last_touch_y, 0)
                self.parent.parent.apply_transform(Matrix().translate(*translation))

    def on_touch_up(self, touch):
        """Called when the user lifts their finger or releases their mouse button"""
        if touch.button == "left":
            self.touch_up_callback()
