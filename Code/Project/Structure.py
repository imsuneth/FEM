import numpy as np
from Element import Element
from Node import *
from ElementTypes import *
from DataStructures import *


class Structure:
    n_elements = None
    elements = None
    nodes = None
    cross_section = None
    element_types = None
    n_sections = 6

    def __init__(self, js):
        # Load the jason file and construct the virtual structure
        # Create Node objects and put them in nparray "nodes"
        n_nodes = js["no_of_nodes"]
        self.nodes = np.empty(n_nodes, dtype=Node)
        js_nodes = js["nodes"]
        for node in js_nodes:
            id = node["id"]
            p_x = node["x"]
            p_y = node["y"]
            p_z = node["z"]
            new_node = Node(id, p_x, p_y, p_z)
            self.nodes.put(id, new_node)

        # Create ElementType objects and put them in nparray "element_types"
        no_of_crosssection_types = js["no_of_crosssection_types"]
        self.element_types = np.empty(no_of_crosssection_types, dtype=ElementType)
        js_element_types = js["element_type"]
        for element_type in js_element_types:
            id = element_type["id"]
            shape = element_type["id"]
            youngs_mod = element_type["youngs_mod"]
            density = element_type["density"]
            dimensions = element_type["dimensions"]
            new_element_type = None
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
        self.elements = np.empty(n_elements, dtype=Element)
        js_elements = js["elements"]
        for element in js_elements:
            id = element["id"]
            start_node_id = element["start_node_id"]
            start_node = self.nodes[start_node_id]
            end_node_id = element["end_node_id"]
            end_node = self.nodes[end_node_id]
            element_type = self.element_types[element["element_type"]]

            #####################################################
            # When updating to 3D take local_x_dir, local_y_dir, local_z_dir form jason
            #####################################################

            new_element = Element(id, start_node, end_node, element_type, self.n_sections)
            self.elements.put(id, new_element)

        no_of_loads = js["no_of_loads"]
        js_loads = js["loads"]
        for load in js_loads:
            id = load["id"]
            node_id = load["point_id"]
            force = load["force"]
            f_x = force["x"]
            f_y = force["y"]
            f_z = force["z"]
            torque = load["torque"]
            m_x = torque["x"]
            m_y = torque["y"]
            m_z = torque["z"]



        return None

    def analyzeStructure(self):
        # initiate analyze and save results to structureXX-out.json

        return None
