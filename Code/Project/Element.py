import numpy as np
from ElementTypes import *


class Element:

    id = None
    start_node = None
    end_node = None
    angle = None
    length = None
    sections = None
    element_type = None
    n_sections = None

    def __init__(self, id, start_node, end_node, element_type, n_sections):
        self.id = id
        self.id = start_node
        self.id = end_node
        self.element_type = element_type
        self.n_sections = n_sections

        self.sections = np.array(n_sections, dtype=ElementType)
