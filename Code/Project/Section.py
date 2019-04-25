import Material
import numpy as np
from Fiber import Fiber


class Section:
    s_h=np.zeros((2,1)) # section force for each section (included as in the paper)
    e_h=np.zeros((2,1)) # section deformation (included as in the paper)
    section_k=None
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

        resistance_force = np.empty((2,1), dtype=np.float_)
        sectional_stiffness = np.empty(shape=(2, 2), dtype=np.float_)

        for fiber_id in range(self.cross_section.no_of_fibers):
            fiber = self.fibers[fiber_id]
            eps = eps_0 - fiber.y * k
            sigma = Material.material_models[fiber.material_id].get_strain(eps)
            A_i = sigma * fiber.area
            resistance_force[0] += A_i
            resistance_force[1] += -1 * A_i * fiber.y
            E_t = Material.material_models[fiber.material_id].get_e(eps)
            sectional_stiffness_00 = E_t * fiber.area
            sectional_stiffness_01 = sectional_stiffness_00 * fiber.y
            sectional_stiffness_11 = sectional_stiffness_01 * fiber.y
            sectional_stiffness[0][0] += sectional_stiffness_00
            sectional_stiffness[0][1] += -1 * sectional_stiffness_01
            sectional_stiffness[1][1] = sectional_stiffness_11
        sectional_stiffness[1][0] = sectional_stiffness[0][1]
        #print("Resistance force")
        # print(resistance_force)
        # print("sectional_stiffness")
        # print(sectional_stiffness)


        return [resistance_force, sectional_stiffness]



