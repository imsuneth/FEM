import numpy as np
from Element import Element
from Node import Node
from ElementTypes import *


class Structure:
    n_elements = None
    elements = None
    nodes = None
    cross_section = None
    element_types = None

    def __init__(self, js):
        # Load the jason file and construct the virtual structure
        # Create Node objects and put them in nparray "nodes"
        n_nodes = js["no_of_nodes"]
        self.nodes = np.array(n_nodes, dtype=Node)
        js_nodes = js["nodes"]
        for node in js_nodes:
            id = node["id"]
            p_x = node["p_x"]
            p_y = node["p_y"]
            p_z = node["p_z"]
            new_node = Node(id, p_x, p_y, p_z)
            self.nodes.put(id, new_node)

        # Create ElementType objects and put them in nparray "element_types"
        no_of_crosssection_types = js["no_of_crosssection_types"]
        self.element_types = np.array(no_of_crosssection_types, dtype=ElementType)
        js_element_types = js["element_type"]
        for element_type in js_element_types:
            id = element_type["id"]
            shape = element_type["id"]
            youngs_mod = element_type["youngs_mod"]
            density = element_type["density"]
            dimensions = element_type["dimensions"]
            if shape == "rectangle":
                width = dimensions["y"]
                height = dimensions["z"]
                new_element_type = SquareElementType(width, height, youngs_mod, density)
            elif shape == "circle":
                radius = dimensions["radius"]
                new_element_type = CircularElementType(radius, youngs_mod, density)
            self.element_types.put(id, new_element_type)

        # Create Element objects and put them in nparray "elements"
        n_elements = js["no_of_elements"]
        self.elements = np.array(n_elements, dtype=Element)
        js_elements = js["elements"]
        for element in js_elements:
            id = element["id"]
            start_node_id = element["start_node_id"]
            end_node_id = element["end_node_id"]
            cross_section =

        return None

    def analyzeStructure(self):
        # initiate analyze and save results to structureXX-out.json

        return None
