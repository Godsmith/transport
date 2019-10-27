from copy import deepcopy
from grid import Grid
from factory import Factory
from resource import Resource
import kivy

kivy.require('1.11.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, InstructionGroup


class GridWidget(Widget):
    def __init__(self, rows, size_hint=None):
        super(GridWidget, self).__init__(size_hint=size_hint)
        self.rows = rows
        self.bind(size=self.update_rect)
        self.gridlines = None

    def update_rect(self, instance, value):
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

    @property
    def cell_width(self):
        return self.width/self.rows

    @property
    def cell_height(self):
        return self.height/self.rows

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
        diffs = [abs(value-val) for val in values]
        return diffs.index(min(diffs))

    def _to_grid_coordinates(self, x, y):
        x_index = self._index_of_closest(x, self.cell_x_centers)
        y_index = self._index_of_closest(y, self.cell_y_centers)
        return list(self.cell_x_centers)[x_index],list(self.cell_y_centers)[y_index]


    def on_touch_down(self, touch):
        x, y = self._to_grid_coordinates(touch.x, touch.y)
        with self.canvas:
            Color(1, 0, 0)
            d = 30.
            Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(x, y))

    def on_touch_move(self, touch):
        x, y = self._to_grid_coordinates(touch.x, touch.y)
        touch.ud['line'].points += [x, y]


class MyPaintApp(App):

    def build(self):
        layout = ScatterLayout(translation_touches=2, do_rotation=False)
        widget = GridWidget(8, size_hint=(1,1))
        layout.add_widget(widget)
        return layout


if __name__ == '__main__':
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
