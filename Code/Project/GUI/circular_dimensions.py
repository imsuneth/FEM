from GUI.dimensions import Dimensions


class CircularDimensions(Dimensions):
    def __init__(self, radius):
        self.radius = float(radius)

    def to_list(self):
        return ['Radius: ' + str(self.radius)]
