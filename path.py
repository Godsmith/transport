class Point(tuple):
    def __init__(self, x, y):
        super(Point, self).__init__((x, y))
        self.x = x
        self.y = y


class Path(list):
    pass
