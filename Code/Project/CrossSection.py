import numpy as np
from Material import Material
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


class CircularCrossSection(CrossSection):

    def __init__(self, id, radius, no_of_fibers, fiber_material_ids):
        self.id = id
        self.radius = radius
        self.no_of_fibers = no_of_fibers
        self.fiber_material_ids = fiber_material_ids
