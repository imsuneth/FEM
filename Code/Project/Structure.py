import numpy as np
from Element import *
from Node import *
from CrossSection import *
from CalculationData import *
from numpy.linalg import inv


class Structure:
    n_sections = 6

    def __init__(self, js):
        # Load the jason file and construct the virtual structure
        # Create Node objects and put them in nparray "nodes"

        # self.n_totalFreeDof = 0 #added by pubudu to extractDOF from deformation increment vector

        self.fix_Point_array = []

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

            angleRatio = element["local_x_dir"]["y"] / element["local_x_dir"]["x"]
            angle = None
            if angleRatio > 0:
                angle = math.atan(angleRatio)
            else:
                angleRatio = -1 * angleRatio
                angle = math.pi - math.atan(angleRatio)

            yDiff = abs(self.nodes[start_node_id].p_y - self.nodes[end_node_id].p_y)
            xDiff = abs(self.nodes[start_node_id].p_x - self.nodes[end_node_id].p_x)
            length = math.sqrt(math.pow(yDiff, 2) + math.pow(xDiff, 2))

            new_element = Element(id, start_node, end_node, cross_section, self.n_sections, angle, length)
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
            self.fix_Point_array += [node_id]
            t_x = translation["x"]
            t_y = translation["y"]
            t_z = translation["z"]

            rotation = fixed_point["rotation"]
            r_x = rotation["x"]
            r_y = rotation["y"]
            r_z = rotation["z"]

            node = self.nodes[node_id]
            [node.t_x, node.t_y, node.t_z, node.r_x, node.r_y, node.r_z] = [t_x, t_y, t_z, r_x, r_y, r_z]

            # self.n_totalFreeDof+=t_x+t_y+r_x+r_y
        return None

    def analyzeStructure(self):
        # initiate analyze and save results to structureXX-out.json
        force = []
        deformation = []
        for node_id in range(self.n_nodes):
            node = self.nodes[node_id]
            force += [node.f_x, node.f_y, node.m_z]
            deformation += [node.d_x, node.d_y, node.dm_z]
        force = np.asarray(force).reshape(self.n_nodes * 3, 1)
        deformation = np.asarray(deformation).reshape(self.n_nodes * 3, 1)
        element = Element
        DOF = 3

        kGlobal = [[0 for a0 in range(DOF * 3)] for a1 in range(DOF * 3)]

        for e in range(self.n_elements):
            ele = self.elements[e]
            startNode = ele.start_node
            endNode = ele.end_node
            Rmatrix = ele.rotMatrix()
            EMatrix = Rmatrix[e]

            y1 = DOF * startNode.id
            y2 = y1 + DOF
            x1 = DOF * startNode.id
            x2 = x1 + DOF
            kGlobal[y1:y2, x1:x2] += EMatrix[:DOF, :DOF]

            y1 = DOF * startNode.id
            y2 = y1 + DOF
            x1 = DOF * endNode.id
            x2 = x1 + DOF
            kGlobal[y1:y2, x1:x2] += EMatrix[:DOF, DOF:]

            y1 = DOF * endNode.id
            y2 = y1 + DOF
            x1 = DOF * startNode.id
            x2 = x1 + DOF
            kGlobal[y1:y2, x1:x2] += EMatrix[DOF:, :DOF]

            y1 = DOF * endNode.id
            y2 = y1 + DOF
            x1 = DOF * endNode.id
            x2 = x1 + DOF
            kGlobal[y1:y2, x1:x2] += EMatrix[DOF:, DOF:]

        full_matrix = kGlobal
        full_force = force
        full_deformation = deformation
        def_for_reuse = []
        deleting_lines = []

        for node_id in sorted(self.fix_Point_array)[::-1]:
            node = self.nodes[node_id]
            Line = DOF * node_id
            if (node.r_z):
                kGlobal = np.delete(kGlobal, Line + 2, 0)
                kGlobal = np.delete(kGlobal, Line + 2, 1)
                force = np.delete(force, Line + 2, 0)
                def_for_reuse = def_for_reuse + [deformation[Line + 2]]
                deleting_lines = deleting_lines + [Line + 2]

            if (node.t_y):
                kGlobal = np.delete(kGlobal, Line + 1, 0)
                kGlobal = np.delete(kGlobal, Line + 1, 1)
                force = np.delete(force, Line + 1, 0)
                def_for_reuse = [deformation[Line + 1]] + def_for_reuse
                deleting_lines += [Line + 1]

            if (node.t_x):
                kGlobal = np.delete(kGlobal, Line, 0)
                kGlobal = np.delete(kGlobal, Line, 1)
                force = np.delete(force, Line, 0)
                def_for_reuse = [deformation[Line]] + def_for_reuse
                deleting_lines += [Line]

            deformation = inv(kGlobal) * force

            for line_index in range(len(deleting_lines)):
                np.insert(deformation, deleting_lines[line_index], def_for_reuse[line_index], axis=0)

            force = full_matrix * deformation

            Rmatrix = element.analyze(force, deformation)

        ###########################################################################################

        DOFcount = 0

        for elementNO in Structure.n_elements:
            numberOfFreeDOF = self.extractDOF(elementNO)
            if numberOfFreeDOF != 0:  # not a complete fixed point %%%%%%%%%% can optimize

                elementDOFdeformation = np.zeros(numberOfFreeDOF, dtype=int)

                count = 1
                while (count == numberOfFreeDOF):
                    elementDOFdeformation.put(count - 1, Struct_def_increment[0][DOFcount])
                    DOFcount += 1
                    count += 1

        ############################################################################################
        return None
