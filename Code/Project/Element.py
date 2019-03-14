import numpy as np
import ElementTypes


class Element:

    id = None
    start_node = None
    end_node = None
    angle = None
    length = None
    sections = None
    n_sections = None

    def __init__(self, id, start_node, end_node, n_sections):
        self.id = id
        self.id = start_node
        self.id = end_node
        self.n_sections = n_sections

        self.sections = np.array(n_sections, dtype=ElementTypes)
