import numpy as np
from Material import Material
from Fiber import Fiber


class CrossSection:
    area = 0

    def analyze(self, section_deformation):
        return None


class SquareCrossSection(CrossSection):

    def __init__(self, id, width, height, no_of_fibers, fiber_material_ids):
        self.resisting_force = np.empty(2, dtype=np.float_)
        self.id = id
        self.width = width
        self.height = height
        self.no_of_fibers = no_of_fibers
        self.fiber_material_ids = fiber_material_ids
        self.fibers = np.empty(no_of_fibers, dtype=Fiber)
        fiber_height = self.height / self.no_of_fibers

        for fiber_id in range(no_of_fibers):
            y = fiber_height * (self.no_of_fibers - 1 - 2 * fiber_id) / 2
            fiber = Fiber(fiber_id, y, self.width, fiber_height, fiber_material_ids[id])
            self.fibers.put(fiber_id, fiber)

        self.analyze(self, [1, 2])

    def analyze(self, section_deformation):
        eps_0 = section_deformation[0]  # centroid strain
        k = section_deformation[1]

        A = 0
        M = 0

        print()

        for fiber_id in range(self.no_of_fibers):
            fiber = self.fibers[fiber_id]
            eps = eps_0 - fiber.y * k
            sigma = Material.getStrainFromStress(fiber.material_id, eps)
            a_fib = fiber.height * fiber.width
            a_i = sigma * a_fib
            A += a_i
            M += -1 * a_i * fiber.y

        return None


class CircularCrossSection(CrossSection):

    def __init__(self, id, radius, no_of_fibers, fiber_material_ids):
        self.id = id
        self.radius = radius
        self.no_of_fibers = no_of_fibers
        self.fiber_material_ids = fiber_material_ids
