import numpy as np
from CrossSection import *


class Element:
    angle = None
    length = None

    def __init__(self, id, start_node, end_node, element_type, n_sections):
        self.id = id
        self.id = start_node
        self.id = end_node
        self.element_type = element_type
        self.n_sections = n_sections

        self.sections = np.array(n_sections, dtype=CrossSection)

    def analyze(self):
        # Pubudu, you code goes here.
        # Get inputs from Imesh as parameters of this function.
        # Get inputs from Me using section.analyze().

        return None
