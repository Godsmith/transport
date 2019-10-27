class Grid:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.entities = {}

    def add(self, entity, position):
        self.entities[position] = entity