from resource import Resource


class Factory:
    def __init__(self, creates: Resource = None, consumes: Resource = None):
        self.creates = creates
        self.consumes = consumes
