from GUI.structure import Structure as Gui_structure
from Node import Node
from CrossSection import *
from Element import Element
from DOF import DOF
import math
import numpy as np


class Interface:

    def __init__(self, structure: Gui_structure):
        self.no_of_crosssection_types = structure.no_of_crosssection_types
        self.no_of_nodes = structure.no_of_nodes
        self.no_of_materials = structure.no_of_materials
        self.no_of_elements = structure.no_of_elements

        self.nodes = np.empty(self.no_of_nodes, dtype=Node)

        for node in structure.nodes_dict:
            id = node.id
            p_x = node.x
            p_y = node.y
            p_z = node.z
            load = node.point_load
            f_x = DOF([load.f_x, load.is_controlled, load.ratio])
            f_y = DOF([load.f_y, load.is_controlled, load.ratio])
            f_z = DOF([load.f_z, load.is_controlled, load.ratio])
            m_x = DOF([load.m_x, load.is_controlled, load.ratio])
            m_y = DOF([load.m_y, load.is_controlled, load.ratio])
            m_z = DOF([load.m_z, load.is_controlled, load.ratio])
            restraint = node.restraint
            t_x = restraint.t1_restrained
            t_y = restraint.t2_restrained
            t_z = restraint.t3_restrained
            r_x = restraint.r1_restrained
            r_y = restraint.r2_restrained
            r_z = restraint.r3_restrained
            new_node = Node(id, p_x, p_y, p_z, f_x, f_y, f_z, m_x, m_y, m_z, t_x, t_y, t_z, r_x, r_y, r_z)
            self.nodes.put(node.id, new_node)

        # Create CrossSection objects and put them in nparray "cross_sections"
        self.cross_sections = np.empty(self.no_of_crosssection_types, dtype=CrossSection)
        for cross_section in structure.concrete_sections_dict:
            id = cross_section.id
            shape = cross_section.shape
            no_of_fibers = cross_section.no_of_fibers
            fiber_material_ids = cross_section.fiber_material_ids
            new_cross_section = None
            if shape == "rectangle":
                width = cross_section.dimensions.width
                height = cross_section.dimensions.heigth
                new_cross_section = SquareCrossSection(id, width, height, no_of_fibers, fiber_material_ids)

            elif shape == "circle":
                radius = cross_section.dimensions.radius
                new_cross_section = CircularCrossSection(id, radius, no_of_fibers, fiber_material_ids)

            self.cross_sections.put(id, new_cross_section)

        # Create Element objects and put them in nparray "elements"
        self.elements = np.empty(self.no_of_elements, dtype=Element)
        for element in structure.elements_dict:
            id = element.id
            start_node_id = element.start_node
            start_node = self.nodes[start_node_id]
            end_node_id = element.end_node
            end_node = self.nodes[end_node_id]
            cross_section = self.cross_sections[element["element_type"]]

            #####################################################
            # When updating to 3D take local_x_dir, local_y_dir, local_z_dir form jason
            #####################################################

            x_cord = element["local_x_dir"]["x"]
            y_cord = element["local_x_dir"]["y"]

            # angleRatio=y_cord/x_cord
            # angle=None
            # if angleRatio>0:
            #     #angle=math.atan(angleRatio)
            #     if(x_cord>0 and y_cord>0):
            #         angle=math.atan(angleRatio)
            #     else:
            #         angle=math.pi+math.atan(angleRatio)
            # else:
            #     if(x_cord<0):
            #         angle=math.pi+math.atan(angleRatio)
            #     else:
            #         angle=2*math.pi+math.atan(angleRatio)
            #
            # # angle = element["angle"]
            angle = 0
            yDiff = abs(start_node.p_y - end_node.p_y)
            xDiff = abs(start_node.p_x - end_node.p_x)

            length = math.sqrt(math.pow(yDiff, 2) + math.pow(xDiff, 2))
            new_element = Element(id, start_node, end_node, cross_section, self.n_sections, angle, length)
            self.elements.put(id, new_element)
