import Material
import numpy as np
from Fiber import Fiber


class Section:
    def __init__(self, id, cross_section):
        self.k_section_initial = None
        self.f_section_resist = None
        self.total_deformation=np.zeros((2,1))
        self.total_force=np.zeros((2,1))
        self.id = id
        self.cross_section = cross_section
        self.fibers = np.empty(cross_section.no_of_fibers, dtype=Fiber)
        fiber_height = cross_section.height / cross_section.no_of_fibers

        for fiber_id in range(cross_section.no_of_fibers):
            y = fiber_height * (cross_section.no_of_fibers - 1 - 2 * fiber_id) / 2
            fiber = Fiber(fiber_id, y, cross_section.width, fiber_height, cross_section.fiber_material_ids[fiber_id])
            self.fibers.put(fiber_id, fiber)

    def analyze(self, section_deformation):
        # print("section_deformation",section_deformation)
        eps_0 = section_deformation[0]  # centroid strain
        k = section_deformation[1]
        # print("eps_0:", eps_0, "k:", k)
        resistance_force = np.zeros((2, 1), dtype=np.float_)
        sectional_stiffness = np.zeros(shape=(2, 2), dtype=np.float_)

        for fiber_id in range(self.cross_section.no_of_fibers):
            fiber = self.fibers[fiber_id]
            # print("section_deformation[1]:", k)
            # print("eps_0:",eps_0)
            eps = eps_0 - fiber.y * k
            sigma = Material.material_models[fiber.material_id].get_strain(eps)
            fiber.eps = eps
            fiber.sigma = sigma
            area = fiber.area
            # print("area:", area)
            # print("fiber:", fiber.id,"y:", fiber.y)
            A_i = sigma * area
            resistance_force[0] += A_i
            resistance_force[1] += -1 * A_i * fiber.y
            E_t = Material.material_models[fiber.material_id].get_e(eps)
            sectional_stiffness_00 = E_t * area
            sectional_stiffness_01 = -E_t * area * fiber.y
            #print("sectional_stiffness_01:", sectional_stiffness_01)
            sectional_stiffness_11 = E_t * area * fiber.y * fiber.y
            sectional_stiffness[0][0] += sectional_stiffness_00
            sectional_stiffness[0][1] += sectional_stiffness_01
            sectional_stiffness[1][1] += sectional_stiffness_11
        sectional_stiffness[1][0] = sectional_stiffness[0][1]

        # if eps_0 == 0 and k == 0:
        # print("f_section_resist:", resistance_force, "k_section_initial:",sectional_stiffness)
        self.f_section_resist = resistance_force
        self.k_section_initial = sectional_stiffness
        # return [resistance_force, sectional_stiffness]