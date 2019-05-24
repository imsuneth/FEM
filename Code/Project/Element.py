import math

import numpy as np
from numpy.linalg import inv
from Section import *
from log_ import *


class Element:
    k_element_initial = None  # initial stiffness matrix refering local co-ordinate system

    def __init__(self, id, start_node, end_node, cross_section, n_sections, angle, length):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.cross_section = cross_section
        self.n_sections = n_sections
        self.angle = angle
        self.length = length
        self.sections = np.empty(n_sections, dtype=Section)

        for section_id in range(n_sections):
            section = Section(section_id, cross_section)
            section.f_section_resist = section.analyze([0, 0])[0]
            section.k_section_initial=section.analyze([0,0])[1]
            self.sections.put(section_id, section)

        if self.n_sections == 3:
            self.wh = [1 / 3, 4 / 3, 1 / 3]
            self.x = [-1, 0, 1]
        elif self.n_sections == 4:
            self.wh = [5 / 6, 1 / 6, 1 / 6, 5 / 6]
            self.x = [-1, - 0.447214, 0.447214, 1]
        elif self.n_sections == 5:
            self.wh = [1 / 10, 49 / 90, 32 / 45, 49 / 90, 1 / 10]
            self.x = [-1, - 0.654654, 0, 0.654654, 1]
        elif self.n_sections == 6:
            self.wh = [0.066667, 0.378475, 0.554858, 0.554858, 0.378475, 0.066667]
            self.x = [-1, - 0.765055, - 0.285232, 0.285232, 0.765055, 1]

    def rotMatrix(self):
        cos = math.cos(self.angle)
        sin = math.sin(self.angle)
        return np.array([[cos, sin, 0, 0, 0, 0],
                         [-sin, cos, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0],
                         [0, 0, 0, cos, sin, 0],
                         [0, 0, 0, -sin, cos, 0],
                         [0, 0, 0, 0, 0, 1]])  # should return the rotational matrix for the element

    def rigidBodyTransMatrix(self):  # L--> length of the element
        L = self.length

        return np.array([[0, 1 / L, 1, 0, -1 / L, 0],
                         [0, 1 / L, 0, 0, -1 / L, 1],
                         [-1, 0, 0, 1, 0, 0]])

    def calInitialElement_K(self, Condition):  # Condition="LOCAL" for refering local co-ordinate system & Condition="GLOBAL" for refering global co-ordinate system

        logger.info("Call element %d initial stiffness matrix" % self.id)

        initialElementFlexibMat = 0

        for section_ in range(self.n_sections):
            Section_K = self.sections[section_].analyze([0, 0])
            NP = np.array([[0, 0, 1],
                           [((self.x[section_] + 1) / 2) - 1, (self.x[section_] + 1) / 2, 0]])
            fh = inv(Section_K[1])
            mat1 = np.transpose(NP) @ fh
            mat2 = mat1 @ NP
            mat3 = mat2 * self.wh[section_]
            mat4 = mat3 * (self.length / 2)
            initialElementFlexibMat += mat4

        k_element_initial = inv(initialElementFlexibMat)

        self.k_element_initial = k_element_initial

        if Condition == "GLOBAL":
            return np.transpose(self.rotMatrix()) @ np.transpose(self.rigidBodyTransMatrix()) @ k_element_initial @ self.rigidBodyTransMatrix() @ self.rotMatrix()  # 6x6 matrix refering global co-ordinate system

        elif Condition == "LOCAL":
            return k_element_initial

    def analyze(self, tolerance):  # for the first iteration set the initial call to True

        logger.info("Element:%d Sectional level iteration running" % self.id)

        elementDefINCR = np.array([self.start_node.d_x, self.start_node.d_y, self.start_node.dm_z, self.end_node.d_x, self.end_node.d_y, self.end_node.dm_z])

        rotate = np.matmul(self.rotMatrix(), elementDefINCR)  # convert defINCR to local co-ordinate systme
        basicSystem = np.matmul(self.rigidBodyTransMatrix(), rotate)  # remove rigid body modes (basicSystem 3x1 matrix)

        elementForceINCR = np.matmul(self.k_element_initial, basicSystem)

        for section_ in range(self.n_sections):  # newton raphson iteration

            logger.info("Element %d sectional iteration running" % self.id)
            section=self.sections[section_]

            NP = np.array([[0, 0, 1], [((self.x[section_] + 1) / 2) - 1, (self.x[section_] + 1) / 2, 0]])

            sectionForceINCR = np.matmul(NP, elementForceINCR)  # sectionForceINCR ---> 2X1 matrix

            sectionDefINCR_ = np.matmul(section.k_section_initial, sectionForceINCR)

            unbalanceForce = sectionForceINCR - section.f_section_resist

            while (self.conditionCheck(unbalanceForce, tolerance)):
                corrective_d = np.matmul(inv(section.k_section_initial), unbalanceForce)
                sectionDefINCR_ += corrective_d
                [section.f_section_resist, section.k_section_initial] = self.sections[section].analyze(sectionDefINCR_)
                sectionForceINCR = np.matmul(section.k_section_initial, sectionDefINCR_)
                unbalanceForce = sectionForceINCR - section.f_section_resist

        K_element = 0

        for section_ in range(self.n_sections):
            section = self.sections[section_]
            NP = np.array([[0, 0, 1], [((self.x[section_] + 1) / 2) - 1, (self.x[section_] + 1) / 2, 0]])
            fh = inv(self.sections[section_].k_section_initial)
            mat1 = np.matmul(np.transpose(NP), fh)
            mat2 = np.matmul(mat1, NP)
            mat3 = mat2 * self.wh[section_]
            mat4 = mat3 * (self.length / 2)
            K_element += mat4

        K_element = inv(K_element)

        return np.transpose(self.rotMatrix()) @ np.transpose(self.rigidBodyTransMatrix()) @ K_element @ self.rigidBodyTransMatrix() @ self.rotMatrix()  # 6x6 matrix refering global co-ordinate system

    def conditionCheck(self, mat, value):
        max_abs_val = abs(max(mat.min(), mat.max(), key=abs))
        logger.info("Checking convergence. max_abs_val = %f" % max_abs_val)
        if max_abs_val > value:
            return True
        else:

            return False
