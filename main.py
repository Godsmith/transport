from copy import deepcopy

from kivy.clock import Clock
from kivy.vector import Vector

from grid import Grid
from path import Path, Point
from factory import Factory
from resource import Resource
import kivy

from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, InstructionGroup


class GridWidget(Widget):
    def __init__(self, grid, size_hint=None):
        super(GridWidget, self).__init__(size_hint=size_hint)
        self.grid = grid
        self.rows = self.grid.height
        self.bind(size=self.update_rect)
        self.gridlines = None
        self.paths = None

    def update(self, dt):
        self.grid.update(dt)
        self._paint_paths()

    def update_rect(self, instance, value):
        self._paint_gridlines()

    def _paint_gridlines(self):
        if self.gridlines:
            self.canvas.remove(self.gridlines)
        self.gridlines = InstructionGroup()
        self.gridlines.add(Color(1, 1, 1))
        for line in range(0, self.rows + 1):
            x = self.cell_width * line
            y = self.cell_height * line
            self.gridlines.add(Line(points=((x, 0), (x, self.height))))
            self.gridlines.add(Line(points=((0, y), (self.width, y))))
        self.canvas.add(self.gridlines)

    def _paint_paths(self):
        if self.paths:
            self.canvas.remove(self.paths)
        self.paths = InstructionGroup()
        self.paths.add(Color(1, 0, 0))
        for grid_path in self.grid.paths:
            new_grid_path = [self._to_coordinates(*point) for point in grid_path]
            self.paths.add(Line(points=new_grid_path))

            d = 30
            x, y = self._position_partway_between_two_cells(
                grid_path.point_agent_is_leaving,
                grid_path.point_agent_is_approaching,
                grid_path.distance_to_next_square,
            )
            self.paths.add(Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d)))
        self.canvas.add(self.paths)

    def _position_partway_between_two_cells(
        self, point1: Point, point2: Point, fraction: float
    ):
        x1, y1 = self._to_coordinates(*point1)
        x2, y2 = self._to_coordinates(*point2)
        return x1 + (x2 - x1) * fraction, y1 + (y2 - y1) * fraction

    @property
    def cell_width(self):
        return self.width / self.rows

    @property
    def cell_height(self):
        return self.height / self.rows

    @property
    def cell_x_centers(self):
        for i in range(0, self.rows + 1):
            yield self.cell_width * (i + 0.5)

    @property
    def cell_y_centers(self):
        for i in range(0, self.rows + 1):
            yield self.cell_height * (i + 0.5)

    @staticmethod
    def _index_of_closest(value, values):
        diffs = [abs(value - val) for val in values]
        return diffs.index(min(diffs))

    def _to_coordinates(self, x_index, y_index):
        return list(self.cell_x_centers)[x_index], list(self.cell_y_centers)[y_index]

    def _to_grid_coordinates(self, x, y):
        x_index = self._index_of_closest(x, self.cell_x_centers)
        y_index = self._index_of_closest(y, self.cell_y_centers)
        return self._to_coordinates(x_index, y_index)

    def on_touch_down(self, touch):
        x, y = self._to_grid_coordinates(touch.x, touch.y)
        x_index = self._index_of_closest(x, self.cell_x_centers)
        y_index = self._index_of_closest(y, self.cell_y_centers)
        self.grid.paths.append(Path(Point(x_index, y_index)))

    def on_touch_move(self, touch):
        x, y = self._to_grid_coordinates(touch.x, touch.y)
        x_index = self._index_of_closest(x, self.cell_x_centers)
        y_index = self._index_of_closest(y, self.cell_y_centers)
        point = Point(x_index, y_index)
        if self.grid.paths[-1][-1] != point:
            self.grid.paths[-1].append(point)


class MyPaintApp(App):
    def build(self):
        layout = ScatterLayout(translation_touches=2, do_rotation=False)
        widget = GridWidget(Grid(8, 8), size_hint=(1, 1))
        Clock.schedule_interval(widget.update, 1.0 / 60.0)
        layout.add_widget(widget)
        return layout


if __name__ == "__main__":
    MyPaintApp().run()

# def main():
#     grid = Grid(10, 10)
#
#     grid.add(Factory(creates=Resource.BLUE))
#     grid.add(Factory(consumes=Resource.BLUE))
#
#
# if __name__ == '__main__':
#     main()
