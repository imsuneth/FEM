import numpy as np
import Element


class Structure:
    n_elements = None
    elements = None

    def __init__(self, js):
        # Load the jason file and construct the virtual structure

        n_elements = js["no_of_elements"]
        self.elements = np.array(n_elements, dtype=Element)

        return None

    def analyzeStructure(self):
        # initiate analyze and save results to structureXX-out.json

        return None
