import math

import numpy as np
from numpy.linalg import inv


class Element:

    def __init__(self, id, start_node, end_node, cross_section, theta_x_e, theta_y_e, theta_z_e, length):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.cross_section = cross_section
        self.length = length
        self.theta_x_e = theta_x_e
        self.theta_y_e = theta_y_e
        self.theta_z_e = theta_z_e
