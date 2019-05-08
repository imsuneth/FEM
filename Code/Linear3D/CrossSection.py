import numpy as np



class CrossSection:
    area = 0


class SquareCrossSection(CrossSection):

    def __init__(self, id, width, height):
        self.resisting_force = np.empty(2, dtype=np.float_)
        self.id = id
        self.width = width
        self.height = height



class CircularCrossSection(CrossSection):

    def __init__(self, id, radius):
        self.id = id
        self.radius = radius

