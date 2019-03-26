import numpy as np
from CrossSection import *


class Element:
    angle = None
    length = None

    def __init__(self, id, start_node, end_node, element_type, n_sections):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.element_type = element_type
        self.n_sections = n_sections

        self.sections = np.empty(n_sections, dtype=CrossSection)

    def analyze(self):
        # Pubudu, you code goes here.
        # Get inputs from Imesh as parameters of this function.
        # Get inputs from Me using section.analyze(section_deformation).

        return None
