import numpy as np
from CrossSection import *
from Section import Section


class Element:
    angle = None
    length = None

    def __init__(self, id, start_node, end_node, cross_section, n_sections):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.cross_section = cross_section
        self.n_sections = n_sections
        self.sections = np.empty(n_sections, dtype=Section)

        for section_id in range(n_sections):
            section = Section(section_id, cross_section)
            self.sections.put(section_id, section)

    def analyze(self):
        # Pubudu, you code goes here.
        # Get inputs from Imesh as parameters of this function.
        # Get inputs from Me using section.analyze(section_deformation).

        return None
