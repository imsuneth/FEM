import numpy as np
from Element import *
from Node import *
from CrossSection import *
from CalculationData import *
from numpy.linalg import inv
from log_ import *
import plotTheStruct


class Structure:
    n_sections = 6
    tolerence = 0.00001
    max_Iterations = 10

    def __init__(self, js):
        # Load the jason file and construct the virtual structure
        # Create Node objects and put them in nparray "nodes"
        logger.info("################################\n")
        logger.info("Creating the Virtual Structure\n")
        logger.info("################################\n")
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
            logger.debug("Node id= %d, Coordinates [%d %d %d]" % (id, p_x, p_y, p_z))
            new_node = Node(id, p_x, p_y, p_z)
            self.nodes.put(id, new_node)

        # logger.info("Node reading --> Done")
        logger.info("Node reading --> Done")

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
                new_cross_section = SquareCrossSection(id, width, height, no_of_fibers, fiber_material_ids)

                logger.debug("Cross Section id:%d\tType:%s\tno of Fibers:%d\twidth=%d\theight:%d" % (
                    id, shape, no_of_fibers, width, height))

            elif shape == "circle":
                radius = dimensions["radius"]
                new_cross_section = CircularCrossSection(id, radius, no_of_fibers, fiber_material_ids)

                logger.debug(
                    "Cross Section id:%d\tType:%s\tno of Fibers:%d\tRadius:%d" % (id, shape, no_of_fibers, radius))

            self.cross_sections.put(id, new_cross_section)

        logger.info("Cross section reading--> Done")

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

            # x_cord=element["local_x_dir"]["x"]
            # y_cord=element["local_x_dir"]["y"]
            #
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
            # print("angle",id)
            # print("angle in degrees=",(180/math.pi)*angle)
            # print("angle in degrees=",angle)
            angle = element["angle"]
            yDiff = abs(self.nodes[start_node_id].p_y - self.nodes[end_node_id].p_y)
            xDiff = abs(self.nodes[start_node_id].p_x - self.nodes[end_node_id].p_x)
            length = math.sqrt(math.pow(yDiff, 2) + math.pow(xDiff, 2))

            # logge# .debug("Element:%d\tLength:%d\tAngle:%d\tno of Sections:%d\tCross section type:%d\tStard node:%d\tEnd node:%d" %(id,length,angle,self.n_sections,cross_section,start_node_id,end_node_id))

            new_element = Element(id, start_node, end_node, cross_section, self.n_sections, angle, length)
            self.elements.put(id, new_element)
        logger.info("Elements Creation --> Done")

        # Take loads applied and assign them to Nodes
        self.no_of_loads = js["no_of_loads"]
        js_loads = js["loads"]
        for load in js_loads:
            # id = load["id"]
            node_id = load["point_id"]
            force = load["force"]
            f_x = DOF(force["x"])
            f_y = DOF(force["y"])
            f_z = DOF(force["z"])
            torque = load["torque"]
            m_x = DOF(torque["x"])
            m_y = DOF(torque["y"])
            m_z = DOF(torque["z"])

            node = self.nodes[node_id]
            [node.f_x, node.f_y, node.f_z, node.m_x, node.m_y, node.m_z] = [f_x, f_y, f_z, m_x, m_y, m_z]
            logger.debug(
                "Load applied node:%d\tForce:[%d %d %d]\tTorque:[%d %d %d]" % (node_id, f_x, f_y, f_z, m_x, m_y, m_z))
        logger.info("Loads Assigning--> Done")
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

            logger.debug("Node %d is Fixed. Translations [t_x=%s,t_y=%s,t_z=%s],Rotations [r_x=%s,r_y=%s,r_z=%s]" % (
                node_id, t_x, t_y, t_z, r_x, r_y, r_z))
            # self.n_totalFreeDof+=t_x+t_y+r_x+r_y
        logger.info("Fixed points Creation--> Done")

        return None

    def analyzeStructure(self):
        # Initial Stiffness - k_0
        DOF_PER_NODE = 3
        mat_size = DOF_PER_NODE * (self.n_elements + 1)
        k_0 = np.zeros([mat_size, mat_size])
        force_vector = np.zeros(mat_size, dtype=np.float_)

        node_order = [-1] * (DOF_PER_NODE * self.n_nodes)
        for element_id in range(self.n_elements):
            element = self.elements[element_id]
            startNode = element.start_node.id
            endNode = element.end_node.id
            k = element.K_element_global()

            y1 = DOF_PER_NODE * startNode
            y2 = y1 + DOF_PER_NODE
            x1 = DOF_PER_NODE * startNode
            x2 = x1 + DOF_PER_NODE
            k_0[y1:y2, x1:x2] += k[:DOF_PER_NODE, :DOF_PER_NODE]

            y1 = DOF_PER_NODE * startNode
            y2 = y1 + DOF_PER_NODE
            x1 = DOF_PER_NODE * endNode
            x2 = x1 + DOF_PER_NODE
            k_0[y1:y2, x1:x2] += k[:DOF_PER_NODE, DOF_PER_NODE:]

            start_node = element.start_node
            force_vector[y1:y2] += start_node.get_dof()
            node_order[y1] = startNode

            y1 = DOF_PER_NODE * endNode
            y2 = y1 + DOF_PER_NODE
            x1 = DOF_PER_NODE * startNode
            x2 = x1 + DOF_PER_NODE
            k_0[y1:y2, x1:x2] += k[DOF_PER_NODE:, :DOF_PER_NODE]

            y1 = DOF_PER_NODE * endNode
            y2 = y1 + DOF_PER_NODE
            x1 = DOF_PER_NODE * endNode
            x2 = x1 + DOF_PER_NODE
            k_0[y1:y2, x1:x2] += k[DOF_PER_NODE:, DOF_PER_NODE:]

            end_node = element.end_node
            force_vector[y1:y2] += end_node.get_dof()
            node_order[y1] = endNode

        node_order = list(filter(lambda a: a != -1, node_order))
        print("Node order:", node_order)
        print("structure_k:", k_0)

        force_vector = list(filter(lambda a: not math.isnan(a), force_vector))


        # Stiffness after applying static loads - k

        for force_id in range(mat_size):
            node_id = node_order[force_id/DOF_PER_NODE]
            if not math.isnan(force_vector[force_id]):
                node = self.nodes[node_id]
                if force_id%DOF_PER_NODE == 0:
                    if not node.f_x.controlled:
                        self.forceControlled(node.f_x.value, force_vector, force_id)



        self.forceControlled()
        self.displacementControlled()

        return None

    def forceControlled(self, force, lforce_vector, force_id):

        return None

    def displacementControlled(self):

        return None
