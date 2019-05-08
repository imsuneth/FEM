import math
import Material
import numpy as np
from numpy.linalg import inv


class Element:

    def __init__(self, id, start_node, end_node, cross_section, material_id, local_dirs):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.cross_section = cross_section
        self.material_id = material_id
        self.local_dirs = local_dirs


        yDiff = abs(start_node.p_y - end_node.p_y)
        xDiff = abs(start_node.p_x - end_node.p_x)
        zDiff = abs(start_node.p_z - end_node.p_z)

        self.length = math.sqrt(math.pow(yDiff, 2) + math.pow(xDiff, 2) + math.pow(zDiff, 2))

        self.theta_x_e = 0
        self.theta_y_e = 0
        self.theta_z_e = 0

    def transform(self):
        l = np.cos(self.theta_x_e)
        m = np.cos(self.theta_y_e)
        n = np.cos(self.theta_z_e)
        D = np.sqrt(np.power(l, 2) + np.power(m, 2))

        return np.array([[l, m, n],
                         [-m / D, l / D, 0],
                         [-l * n / D, -m * n / D, D]])

    def K_element_local(self):
        # mat_1 = E * A / L * np.array([[1, -1],
        #                               [-1, 1]])
        # mat_2 = G * J / L * np.array([[1, -1],
        #                               [-1, 1]])
        # c1 = (E * Iz) / (L)  # value of mat_3
        # c2 = (E * Iz) / (L ** 2)  # value of mat_3
        # c3 = (E * Iz) / (L ** 3)
        #
        # mat_3 = np.array([[12 * c3, 6 * c2, -12 * c3, 6 * c2],
        #                   [6 * c2, 4 * c1, -6 * c2, 2 * c1],
        #                   [-12 * c3, -6 * c2, 125 * c3, -6 * c2],
        #                   [6 * c2, 2 * c1, -6 * c2, 4 * c1]])
        #
        # b1 = (E * Iy) / (L)  # value of mat_4
        # b2 = (E * Iy) / (L ** 2)  # value of mat_4
        # b3 = (E * Iy) / (L ** 3)  # value of mat_4
        #
        # mat_4 = np.array([[12 * b3, -6 * b2, -12 * b3, -6 * b2],
        #                   [-6 * b2, 4 * b1, 6 * b2, 2 * b1],
        #                   [-12 * b3, 6 * b2, 12 * b3, 6 * b2],
        #                   [-6 * b2, 2 * b1, 6 * b2, 4 * b1]])

        material=Material.material_models[self.material_id]

        E=material.get_e #young's modulus
        G=material.get_g # shear modulus
        A=self.cross_section.get_area() # area of the cross section
        L=self.length # element length

        intertia=self.cross_section.calculate_inertia()

        J=intertia[0]
        Iy=intertia[1]
        Iz=intertia[2]

        a = E * A / L
        b = G * J / L

        c3 = (E * Iz) / (L ** 3)
        c2 = (E * Iz) / (L ** 2)  # value of mat_3
        c1 = (E * Iz) / (L)  # value of mat_3

        d3 = (E * Iy) / (L ** 3)  # value of mat_4
        d2 = (E * Iy) / (L ** 2)  # value of mat_4
        d1 = (E * Iy) / (L)  # value of mat_4

        #local_k_mat 12*12 element matrix
        local_k_mat = np.array([[a, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0],

                        [0, 12 * c3, 0, 0, 0, 6 * c2, 0, -12 * c3, 0, 0, 0, 6 * c2],

                        [0, 0, 12 * d3, 0, -6 * d2, 0, 0, 0, -12 * d3, 0, -6 * d2, 0],

                        [0, 0, 0, b, 0, 0, 0, 0, 0, -b, 0, 0],

                        [0, 0, 0, 0, 4 * d1, 0, 0, 0, 6 * d2, 0, 2 * d1, 0],

                        [0, 6 * c2, 0, 0, 0, 4 * c1, 0, -6 * c2, 0, 0, 0, 2 * c1],

                        [-a, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0],

                        [0, -12 * c3, 0, 0, 0, -6 * c2, 0, 12 * c3, 0, 0, 0, -6 * c2],

                        [0, 0, -12 * d3, 0, 6 * d2, 0, 0, 0, 12 * d3, 0, 6 * d2, 0],

                        [0, 0, 0, -b, 0, 0, 0, 0, 0, b, 0, 0],

                        [0, 0, -6 * d2, 0, 2 * d1, 0, 0, 0, 6 * d2, 0, 4 * d1, 0],

                        [0, 6 * c2, 0, 0, 0, 2 * c1, 0, -6 * c2, 0, 0, 0, 4 * c1]])
        return local_k_mat

    def K_element_global(self):
        return np.transpose(self.transform()) * self.K_element_local() * self.transform()
