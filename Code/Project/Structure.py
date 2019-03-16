import numpy as np
from Element import Element
from Node import *
from CrossSection import *
from Material import *


class Structure:
    n_sections = 6

    def __init__(self, js):
        # Load the jason file and construct the virtual structure
        # Create Node objects and put them in nparray "nodes"
        self.n_nodes = js["no_of_nodes"]
        self.nodes = np.empty(self.n_nodes, dtype=Node)
        js_nodes = js["nodes"]
        for node in js_nodes:
            id = node["id"]
            p_x = node["x"]
            p_y = node["y"]
            p_z = node["z"]
            new_node = Node(id, p_x, p_y, p_z)
            self.nodes.put(id, new_node)

        # Create Material objects and put them in nparray "materials"
        self.no_of_materials = js["no_of_materials"]
        self.materials = np.empty(self.no_of_materials, dtype=Material)
        js_materials = js["materials"]
        for material in js_materials:
            id = material["id"]
            name = material["name"]
            youngs_mod = material["youngs_mod"]
            new_material = Material(id, name, youngs_mod)
            self.materials.put(id, new_material)

        # Create CrossSection objects and put them in nparray "cross_sections"
        self.no_of_crosssection_types = js["no_of_crosssection_types"]
        self.cross_sections = np.empty(self.no_of_crosssection_types, dtype=CrossSection)
        js_cross_sections = js["cross_sections"]
        for cross_section in js_cross_sections:
            id = cross_section["id"]
            shape = cross_section["shape"]
            dimensions = cross_section["dimensions"]
            no_of_fibers = cross_section["no_of_fibers"]
            fiber_material_ids = cross_section["fiber_material_ids"]
            new_cross_section = None
            if shape == "rectangle":
                width = dimensions["y"]
                height = dimensions["z"]
                new_cross_section = SquareCrossSection(self, width, height, no_of_fibers, fiber_material_ids)
            elif shape == "circle":
                radius = dimensions["radius"]
                new_cross_section = CircularCrossSection(self, radius, no_of_fibers, fiber_material_ids)
            self.cross_sections.put(id, new_cross_section)

        # Create Element objects and put them in nparray "elements"
        self.n_elements = js["no_of_elements"]
        self.elements = np.empty(self.n_elements, dtype=Element)
        js_elements = js["elements"]
        for element in js_elements:
            id = element["id"]
            start_node_id = element["start_node_id"]
            start_node = self.nodes[start_node_id]
            end_node_id = element["end_node_id"]
            end_node = self.nodes[end_node_id]
            cross_section = self.cross_sections[element["element_type"]]

            #####################################################
            # When updating to 3D take local_x_dir, local_y_dir, local_z_dir form jason
            #####################################################

            new_element = Element(id, start_node, end_node, cross_section, self.n_sections)
            self.elements.put(id, new_element)

        # Take loads applied and assign them to Nodes
        self.no_of_loads = js["no_of_loads"]
        js_loads = js["loads"]
        for load in js_loads:
            # id = load["id"]
            node_id = load["point_id"]
            force = load["force"]
            f_x = force["x"]
            f_y = force["y"]
            f_z = force["z"]
            torque = load["torque"]
            m_x = torque["x"]
            m_y = torque["y"]
            m_z = torque["z"]

            node = self.nodes[node_id]
            [node.f_x, node.f_y, node.f_z, node.m_x, node.m_y, node.m_z] = [f_x, f_y, f_z, m_x, m_y, m_z]

        # Take fixed points and assign nodes as fixed
        self.no_of_fixed_points = js["no_of_fixed_points"]
        js_fixed_points = js["fixed_points"]
        for fixed_point in js_fixed_points:
            # id = fixed_point["id"]
            node_id = fixed_point["point_id"]
            translation = fixed_point["translation"]
            t_x = translation["x"]
            t_y = translation["y"]
            t_z = translation["z"]
            rotation = fixed_point["rotation"]
            r_x = rotation["x"]
            r_y = rotation["y"]
            r_z = rotation["z"]

            node = self.nodes[node_id]
            [node.t_x, node.t_y, node.t_z, node.r_x, node.r_y, node.r_z] = [t_x, t_y, t_z, r_x, r_y, r_z]

        return None

    def analyzeStructure(self):
        # initiate analyze and save results to structureXX-out.json

        # Imesh, your code goes here
        # Get inputs from pubudu using element.analyze()
        # passing necessary parameters to him.

        return None
