from path import Path


class Grid:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.entities = {}
        self.paths = []

    def add(self, entity, position):
        self.entities[position] = entity

    def add_path(self, path: Path):
        self.paths.append(path)
