"""Main entry point for the program"""

# pragma: no cover
from transport.controller import Controller
from transport.model.factory import Factory
from transport.model.grid import Grid
from transport.model.resource import Resource
from transport.view.app import TransportAppView
from transport.view.grid_widget import GridWidget

if __name__ == "__main__":  # pragma: no cover
    WIDTH = 16
    GRID = Grid(WIDTH, WIDTH)
    GRID.add(Factory(x=5, y=5, creates=Resource.BLUE))
    GRID.add(Factory(x=10, y=10, consumes=Resource.BLUE))
    Controller(GRID, TransportAppView(GridWidget(WIDTH))).run()
