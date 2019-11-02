"""Main entry point for the program"""

# pragma: no cover
from transport.controller import Controller
from transport.model.factory import Factory
from transport.model.grid import Grid
from transport.model.path import Point
from transport.model.resource import Resource
from transport.view.app import TransportAppView
from transport.view.grid_widget import GridWidget

if __name__ == "__main__":  # pragma: no cover
    WIDTH = 16
    GRID = Grid(WIDTH, WIDTH)
    GRID.add(Factory(creates=Resource.BLUE), Point(5, 5))
    GRID.add(Factory(consumes=Resource.BLUE), Point(10, 10))
    Controller(GRID, TransportAppView(GridWidget(WIDTH))).run()
