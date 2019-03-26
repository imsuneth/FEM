from Material import Material
import numpy as np
from Fiber import Fiber


class Section:
    def __init__(self, id, cross_section):
        self.id = id
        self.cross_section = cross_section
        self.fibers = np.empty(cross_section.no_of_fibers, dtype=Fiber)
        fiber_height = self.height / self.no_of_fibers

        for fiber_id in range(cross_section.no_of_fibers):
            y = fiber_height * (self.no_of_fibers - 1 - 2 * fiber_id) / 2
            fiber = Fiber(fiber_id, y, self.width, fiber_height, cross_section.fiber_material_ids[fiber_id])
            self.fibers.put(fiber_id, fiber)

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
