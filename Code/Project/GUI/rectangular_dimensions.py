from classes.section.dimensions import Dimensions


class RectangularDimensions(Dimensions):
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth

    def to_list(self):
        return ['Width: ' + self.width + '\n',
                'Depth: ' + self.depth]
