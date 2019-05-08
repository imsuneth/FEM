import math

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

    def K_element_local(self, E, A, L, G, T, Iy, Iz):
        mat_1 = E * A / L * np.array([[1, -1],
                                      [-1, 1]])
        mat_2 = G * T / L * np.array([[1, -1],
                                      [-1, 1]])
        c1 = (E * Iz) / (L)  # value of mat_3
        c2 = (E * Iz) / (L ** 2)  # value of mat_3
        c3 = (E * Iz) / (L ** 3)

        mat_3 = np.array([[12 * c3, 6 * c2, -12 * c3, 6 * c2],
                          [6 * c2, 4 * c1, -6 * c2, 2 * c1],
                          [-12 * c3, -6 * c2, 125 * c3, -6 * c2],
                          [6 * c2, 2 * c1, -6 * c2, 4 * c1]])

        b1 = (E * Iy) / (L)  # value of mat_4
        b2 = (E * Iy) / (L ** 2)  # value of mat_4
        b3 = (E * Iy) / (L ** 3)  # value of mat_4

        mat_4 = np.array([[12 * b3, -6 * b2, -12 * b3, -6 * b2],
                          [-6 * b2, 4 * b1, 6 * b2, 2 * b1],
                          [-12 * b3, 6 * b2, 12 * b3, 6 * b2],
                          [-6 * b2, 2 * b1, 6 * b2, 4 * b1]])

    def K_element_global(self):
        return np.transpose(self.transform()) * self.K_element_local() * self.transform()
