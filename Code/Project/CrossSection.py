import numpy as np
from Fiber import Fiber


class CrossSection:
    area = 0


class SquareCrossSection(CrossSection):

    def __init__(self, id, width, height, no_of_fibers, fiber_material_ids):
        self.resisting_force = np.empty(2, dtype=np.float_)
        self.id = id
        self.width = width
        self.height = height
        self.no_of_fibers = no_of_fibers
        self.fiber_material_ids = fiber_material_ids
        fiber_height = height/no_of_fibers
        self.fiber_areas = np.array([fiber_height]*no_of_fibers)


class CircularCrossSection(CrossSection):

    def __init__(self, id, radius, no_of_fibers, fiber_material_ids):
        self.id = id
        self.radius = radius
        self.no_of_fibers = no_of_fibers
        self.fiber_material_ids = fiber_material_ids
        self.fiber_areas = np.empty(no_of_fibers, dtype=np.float_)
