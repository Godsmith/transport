"""Main entry point for the program"""

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, InstructionGroup
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.widget import Widget

from kivy.graphics.vertex_instructions import Rectangle

from transport.factory import Factory
from transport.path import Path, Point

from transport.grid import Grid
from transport.resource import Resource

COLOR_FROM_RESOURCE = {
    Resource.BLUE: Color(0, 1, 1),
    Resource.RED: Color(1, 0, 0),
    None: Color(0.2, 0.2, 0.2),
}


class GridWidget(Widget):
    """The main grid of the game."""

    def __init__(self, grid):
        super(GridWidget, self).__init__()
        self.grid = grid
        self.rows = self.grid.height
        self.bind(size=self._repaint_gridlines)
        self.gridlines = None
        self.paths = None
        self.entity_instruction_groups = []

    def update(self, dt):
        """Update all contents to the next frame"""
        self.grid.update(dt)
        self._paint_paths()
        self._paint_entities()

    def _repaint_gridlines(self, instance, value):  # pylint: disable=unused-argument
        self._paint_gridlines()

    def _paint_gridlines(self):
        if self.gridlines:
            self.canvas.remove(self.gridlines)
        self.gridlines = InstructionGroup()
        self.gridlines.add(Color(1, 1, 1))
        for line in range(0, self.rows + 1):
            x = self._cell_width * line
            y = self._cell_height * line
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

            d = 15
            x, y = self._position_partway_between_two_cells(
                grid_path.point_agent_is_leaving,
                grid_path.point_agent_is_approaching,
                grid_path.distance_to_next_square,
            )
            self.paths.add(Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d)))
        self.canvas.add(self.paths)

    def _paint_entities(self):
        for instruction_group in self.entity_instruction_groups:
            self.canvas.remove(instruction_group)
        self.entity_instruction_groups = []

        for position, entity in self.grid.entities.items():
            instruction_groups = self._paint_divided_square(
                position.x,
                position.y,
                top_color=COLOR_FROM_RESOURCE[entity.consumes],
                bottom_color=COLOR_FROM_RESOURCE[entity.creates],
            )
            self.entity_instruction_groups.extend(instruction_groups)

        for instruction_group in self.entity_instruction_groups:
            self.canvas.add(instruction_group)

    def _paint_divided_square(
        self, x_index: int, y_index: int, top_color: Color, bottom_color: Color
    ):
        instruction_group = InstructionGroup()
        x, y = self._to_coordinates(x_index, y_index)
        bottom_left_x = x - self._cell_width / 2
        bottom_left_y = y - self._cell_height / 2
        instruction_group.add(bottom_color)
        instruction_group.add(
            Rectangle(
                pos=(bottom_left_x, bottom_left_y),
                size=(self._cell_width, self._cell_height / 2),
            )
        )

        instruction_group2 = InstructionGroup()
        middle_left_y = y
        instruction_group2.add(top_color)
        instruction_group2.add(
            Rectangle(
                pos=(bottom_left_x, middle_left_y),
                size=(self._cell_width, self._cell_height / 2),
            )
        )
        return [instruction_group, instruction_group2]

    def _position_partway_between_two_cells(
        self, point1: Point, point2: Point, fraction: float
    ):
        x1, y1 = self._to_coordinates(*point1)
        x2, y2 = self._to_coordinates(*point2)
        return x1 + (x2 - x1) * fraction, y1 + (y2 - y1) * fraction

    @property
    def _cell_width(self):
        return self.width / self.rows

    @property
    def _cell_height(self):
        return self.height / self.rows

    @property
    def _cell_x_centers(self):
        for i in range(0, self.rows + 1):
            yield self._cell_width * (i + 0.5)

    @property
    def _cell_y_centers(self):
        for i in range(0, self.rows + 1):
            yield self._cell_height * (i + 0.5)

    @staticmethod
    def _index_of_closest(value, values):
        diffs = [abs(value - val) for val in values]
        return diffs.index(min(diffs))

    def _to_coordinates(self, x_index, y_index):
        return list(self._cell_x_centers)[x_index], list(self._cell_y_centers)[y_index]

    def _to_grid_coordinates(self, x, y):
        x_index = self._index_of_closest(x, self._cell_x_centers)
        y_index = self._index_of_closest(y, self._cell_y_centers)
        return self._to_coordinates(x_index, y_index)

    def on_touch_down(self, touch):
        """Called when someone clicks or touches the widget."""
        x, y = self._to_grid_coordinates(touch.x, touch.y)
        x_index = self._index_of_closest(x, self._cell_x_centers)
        y_index = self._index_of_closest(y, self._cell_y_centers)
        self.grid.paths.append(Path(Point(x_index, y_index)))

    def on_touch_move(self, touch):
        """Called when, after a touch down, someone drags inside the widget."""
        x, y = self._to_grid_coordinates(touch.x, touch.y)
        x_index = self._index_of_closest(x, self._cell_x_centers)
        y_index = self._index_of_closest(y, self._cell_y_centers)
        point = Point(x_index, y_index)
        if self.grid.paths[-1][-1] != point:
            self.grid.paths[-1].append(point)


class MyPaintApp(App):
    """The main app of the game."""

    def build(self):  # pylint: disable=no-self-use; # pragma: no cover
        """Called when the app is created."""
        layout = ScatterLayout(translation_touches=2, do_rotation=False)
        widget = GridWidget(self._grid())
        Clock.schedule_interval(widget.update, 1.0 / 60.0)
        layout.add_widget(widget)
        return layout

    @staticmethod
    def _grid():
        grid = Grid(16, 16)
        grid.add(Factory(creates=Resource.BLUE), Point(5, 5))
        grid.add(Factory(consumes=Resource.BLUE), Point(10, 10))
        return grid


if __name__ == "__main__":  # pragma: no cover
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
