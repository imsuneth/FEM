from Material import *
import numpy as np
from Fiber import Fiber


class Section:
    def __init__(self, id, cross_section):
        self.id = id
        self.cross_section = cross_section
        self.fibers = np.empty(cross_section.no_of_fibers, dtype=Fiber)
        fiber_height = cross_section.height / cross_section.no_of_fibers

        for fiber_id in range(cross_section.no_of_fibers):
            y = fiber_height * (cross_section.no_of_fibers - 1 - 2 * fiber_id) / 2
            fiber = Fiber(fiber_id, y, cross_section.width, fiber_height, cross_section.fiber_material_ids[fiber_id])
            self.fibers.put(fiber_id, fiber)

    def analyze(self, section_deformation):
        eps_0 = section_deformation[0]  # centroid strain
        k = section_deformation[1]

        resistance_force = np.empty(2, dtype=float)
        sectional_stiffness = np.empty(shape=(2, 2))

        for fiber_id in range(self.cross_section.no_of_fibers):
            fiber = self.fibers[fiber_id]
            eps = eps_0 - fiber.y * k
            sigma = get_strain_from_stress(fiber.material_id, eps)
            A_fib = fiber.height * fiber.width
            A_i = sigma * A_fib
            resistance_force[0] += A_i
            resistance_force[1] += -1 * A_i * fiber.y

            E_t = get_e(fiber.material_id, eps)
            sectional_stiffness_00 = E_t * A_fib
            sectional_stiffness_01 = sectional_stiffness_00 * fiber.y
            sectional_stiffness_11 = sectional_stiffness_01 * fiber.y
            sectional_stiffness[0][0] = sectional_stiffness_00
            sectional_stiffness[0][1] = sectional_stiffness[1][0] = -1 * sectional_stiffness_01
            sectional_stiffness[1][1] = sectional_stiffness_11

        return [resistance_force, sectional_stiffness]
