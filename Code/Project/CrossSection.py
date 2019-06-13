import numpy as np


class CrossSection:
    area = 0


class SquareCrossSection(CrossSection):

    def __init__(self, id, width, height, no_of_fibers, material_id, reinforcements):
        self.resisting_force = np.zeros(2, dtype=np.float_)
        self.id = id
        self.width = width
        self.height = height
        self.no_of_fibers = no_of_fibers
        self.material_id = material_id
        self.reinforcements = reinforcements
        fiber_height = height/no_of_fibers
        self.fiber_areas = np.array([fiber_height]*no_of_fibers)


class CircularCrossSection(CrossSection):

    def __init__(self, id, radius, no_of_fibers, material_id, reinforcements):
        self.id = id
        self.radius = radius
        self.no_of_fibers = no_of_fibers
        self.material_id = material_id
        self.reinforcements = reinforcements
        self.fiber_areas = np.zeros(no_of_fibers, dtype=np.float_)
