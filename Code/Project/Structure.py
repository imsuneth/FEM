from Element import *
from Node import *
from CrossSection import *
from Reinforcement import *
from DOF import *
from matplotlib import pyplot as plt


class Structure:
    n_sections = 6
    tolerence = 0.00001
    max_Iterations = 10

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
            material_id = cross_section["material_id"]
            no_reinforcements = cross_section["no_reinforcements"]
            reinforcements = cross_section["reinforcements"]
            reinf = np.empty(no_reinforcements, dtype=Reinforcement)
            for reinforcement in reinforcements:
                r_id = reinforcement["id"]
                r_material_id = reinforcement["material_id"]
                distance_from_center = reinforcement["distance_from_center"]
                area = reinforcement["area"]
                new_reinforcement = Reinforcement(r_material_id, distance_from_center, area)
                reinf.put(r_id, new_reinforcement)

            if shape == "rectangle":
                width = dimensions["z"]
                height = dimensions["y"]
                new_cross_section = SquareCrossSection(id, width, height, no_of_fibers, material_id, reinf)

            elif shape == "circle":
                radius = dimensions["radius"]
                new_cross_section = CircularCrossSection(id, radius, no_of_fibers, material_id, reinf)

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

            # logge# .debug("Element:%d\tLength:%d\tAngle:%d\tno of Sections:%d\tCross section type:%d\tStard node:%d\tEnd node:%d" %(id,length,angle,self.n_sections,cross_section,start_node_id,end_node_id))

            new_element = Element(id, start_node, end_node, cross_section, self.n_sections, angle, length)
            self.elements.put(id, new_element)

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

        # initiating necessary variables
        self.DOF_PER_NODE = 3
        self.node_order = None
        self.structure_k = None
        self.force_vector = None
        self.restraints = None
        self.deformation_vector = None
        self.static_force_step = 1
        self.is_force_controlled_analysis = True
        self.force_step_no = 0
        self.total_force_vector = None
        self.total_deformations = None
        self.mat_size = None

        return None

    def analyze_structure(self):

        self.mat_size = self.DOF_PER_NODE * (self.n_elements + 1)
        self.structure_k = np.zeros([self.mat_size, self.mat_size])
        self.force_vector = np.zeros(self.mat_size, dtype=np.float_).transpose()
        self.restraints = np.zeros(self.mat_size, dtype=np.float_).transpose()
        self.deformation_vector = np.zeros(self.mat_size, dtype=np.float_).transpose()

        # Fill initial force_vector, initial structure_k and node_order
        self.assemble_structure_k(0)
        controlled_force_info = []

        # Calculate stiffness after applying static loads
        for force_id in range(self.mat_size):
            node_id = self.node_order[int(math.floor(force_id / self.DOF_PER_NODE))]
            if not math.isnan(self.restraints[force_id]):
                node = self.nodes[node_id]
                if force_id % self.DOF_PER_NODE == 0:
                    if node.f_x.controlled:
                        controlled_force_info.append([node_id, force_id, 0])
                    else:
                        self.force_controlled(node.f_x.value, force_id)

                elif force_id % self.DOF_PER_NODE == 1:
                    if node.f_y.controlled:
                        controlled_force_info.append([node_id, force_id, 1])
                    else:
                        self.force_controlled(node.f_y.value, force_id)

                elif force_id % self.DOF_PER_NODE == 2:
                    if node.m_z.controlled:
                        controlled_force_info.append([node_id, force_id, 2])
                    else:
                        self.force_controlled(node.m_z.value, force_id)

        # Calculate stiffness applying control loads
        for controlled_force in controlled_force_info:
            node_id = controlled_force[0]
            node = self.nodes[node_id]
            force_id = controlled_force[1]
            direction = controlled_force[2]

            if self.is_force_controlled_analysis:
                if direction == 0:
                    self.force_controlled(node.f_x.value, force_id)
                elif direction == 1:
                    self.force_controlled(node.f_y.value, force_id)
                elif direction == 2:
                    self.force_controlled(node.f_z.value, force_id)

            else:
                if direction == 0:
                    self.displacement_controlled(node.f_x.value, force_id)
                elif direction == 1:
                    self.displacement_controlled(node.f_y.value, force_id)
                elif direction == 2:
                    self.displacement_controlled(node.f_z.value, force_id)

        return None

    def force_controlled(self, force, force_id):
        if force == 0:
            return
        self.static_force_step = self.static_force_step * force / abs(force)
        applied_force = self.static_force_step
        self.force_vector[force_id] = self.static_force_step
        # print("force step no:", self.force_step_no)

        # Find initial deformation
        [structure_k_copy, force_vector_copy] = self.apply_boundary_conditions()
        deformation = np.matmul(np.linalg.inv(structure_k_copy), force_vector_copy)
        self.assemble_deformation_vector(deformation)
        self.force_vector = np.matmul(self.structure_k, self.deformation_vector)
        self.save_deformations(self.deformation_vector)

        self.total_force_vector = np.array(self.force_vector)
        self.total_deformations = np.array(self.deformation_vector)

        while abs(applied_force) <= abs(force):
            self.force_step_no += 1
            applied_force += self.static_force_step
            #print("force step no:", self.force_step_no)

            self.assemble_structure_k(1)

            resisting_force = np.matmul(self.structure_k, self.deformation_vector)
            unbalanced_force = self.force_vector - resisting_force

            #print("Structure level Iteration starts:")
            loop_count_structure = 0
            while self.condition_check(unbalanced_force, 0.1):
                reduced_structure_k = self.apply_boundary_conditions_k(self.structure_k)
                reduced_unbalanced_force = self.apply_boundary_conditions_force(unbalanced_force)
                corrective_deformation = np.matmul(np.linalg.inv(reduced_structure_k), reduced_unbalanced_force)
                deformation += corrective_deformation
                self.assemble_deformation_vector(deformation)
                self.save_deformations(self.deformation_vector)
                self.assemble_structure_k(1)
                resisting_force = np.matmul(self.structure_k, self.deformation_vector)
                unbalanced_force = self.force_vector - resisting_force
                loop_count_structure += 1

            #print("structure level iterations ends =", loop_count_structure)
            deformation.fill(0)

            self.total_force_vector += np.matmul(self.structure_k, self.deformation_vector)
            self.total_deformations += self.deformation_vector

            x_value = abs(self.total_deformations[force_id])
            y_value = abs(self.total_force_vector[force_id])
            # print("x:", x_value, "y:", y_value)
            plt.scatter(x_value, y_value)
            plt.pause(0.01)

        self.save_deformations(self.total_deformations)
        self.save_forces(self.total_force_vector)
        plt.show()

    def displacement_controlled(self, force, force_id):
        return None

    def condition_check(self, mat, value):
        max_abs_val = abs(max(mat.min(), mat.max(), key=abs))

        if max_abs_val > value:
            return True
        else:
            return False

    def assemble_deformation_vector(self, deformation):
        index_def = 0
        for index_force in range(self.mat_size):
            if not math.isnan(self.restraints[index_force]):
                self.deformation_vector[index_force] = deformation[index_def]
                index_def += 1

    def assemble_structure_k(self, tag):
        if tag == 0:
            self.node_order = [-1] * (self.DOF_PER_NODE * self.n_nodes)

        for element_id in range(self.n_elements):
            element = self.elements[element_id]
            start_node_id = element.start_node.id
            end_node_id = element.end_node.id

            if tag == 0:
                k = element.calInitialElement_K()
            else:
                k = element.analyze(0.1)

            y1 = self.DOF_PER_NODE * start_node_id
            y2 = y1 + self.DOF_PER_NODE
            x1 = self.DOF_PER_NODE * start_node_id
            x2 = x1 + self.DOF_PER_NODE
            self.structure_k[y1:y2, x1:x2] += k[:self.DOF_PER_NODE, :self.DOF_PER_NODE]

            y1 = self.DOF_PER_NODE * start_node_id
            y2 = y1 + self.DOF_PER_NODE
            x1 = self.DOF_PER_NODE * end_node_id
            x2 = x1 + self.DOF_PER_NODE
            self.structure_k[y1:y2, x1:x2] += k[:self.DOF_PER_NODE, self.DOF_PER_NODE:]

            if tag == 0:
                start_node = element.start_node
                self.force_vector[y1:y2] = start_node.get_dof()
                self.node_order[y1] = start_node_id

            y1 = self.DOF_PER_NODE * end_node_id
            y2 = y1 + self.DOF_PER_NODE
            x1 = self.DOF_PER_NODE * start_node_id
            x2 = x1 + self.DOF_PER_NODE
            self.structure_k[y1:y2, x1:x2] += k[self.DOF_PER_NODE:, :self.DOF_PER_NODE]

            y1 = self.DOF_PER_NODE * end_node_id
            y2 = y1 + self.DOF_PER_NODE
            x1 = self.DOF_PER_NODE * end_node_id
            x2 = x1 + self.DOF_PER_NODE
            self.structure_k[y1:y2, x1:x2] += k[self.DOF_PER_NODE:, self.DOF_PER_NODE:]

            if tag == 0:
                end_node = element.end_node
                self.force_vector[y1:y2] = end_node.get_dof()
                self.node_order[y1] = end_node_id
        if tag == 0:
            self.node_order = list(filter(lambda a: a != -1, self.node_order))
            np.where(self.force_vector is not None, 0, self.force_vector)
            self.restraints = np.array(self.force_vector)

    def save_deformations(self, deformation_vector):
        for node_id in self.node_order:
            from_i = node_id * self.DOF_PER_NODE
            node = self.nodes[node_id]
            node.d_x = deformation_vector[from_i]
            node.d_y = deformation_vector[from_i + 1]
            node.dm_z = deformation_vector[from_i + 2]

    def save_forces(self, force_vector):
        for node_id in self.node_order:
            from_i = node_id * self.DOF_PER_NODE
            node = self.nodes[node_id]
            node.f_x = force_vector[from_i]
            node.f_y = force_vector[from_i + 1]
            node.m_z = force_vector[from_i + 2]

    def apply_boundary_conditions(self):
        # Applying boundary conditions
        force_vector_copy = self.force_vector
        structure_k_copy = self.structure_k
        index = 0
        for force in self.restraints:
            if math.isnan(force):
                structure_k_copy = np.delete(structure_k_copy, index, 0)
                structure_k_copy = np.delete(structure_k_copy, index, 1)
                force_vector_copy = np.delete(force_vector_copy, index, 0)
            else:
                index += 1

        return [structure_k_copy, force_vector_copy]

    def apply_boundary_conditions_force(self, force_vector):
        # Applying boundary conditions
        force_vector_copy = force_vector
        index = 0
        for force in self.restraints:
            if math.isnan(force):
                force_vector_copy = np.delete(force_vector_copy, index, 0)
            else:
                index += 1
        return force_vector_copy

    def apply_boundary_conditions_k(self, stiffness):
        # Applying boundary conditions
        structure_k_copy = stiffness
        index = 0
        for force in self.restraints:
            if math.isnan(force):
                structure_k_copy = np.delete(structure_k_copy, index, 0)
                structure_k_copy = np.delete(structure_k_copy, index, 1)
            else:
                index += 1
        return structure_k_copy
