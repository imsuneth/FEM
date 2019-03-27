import math

import numpy as np
from CrossSection import *
from Structure import *
from Node import *
from Main import *
from Section import *

class Element:
    angle = None
    length = None

    def __init__(self, id, start_node, end_node, cross_section, n_sections,angle,length):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.cross_section = cross_section
        self.n_sections = n_sections
        self.angle=angle
        self.length=length
        self.sections = np.empty(n_sections, dtype=Section)

        for section_id in range(n_sections):
            section = Section(section_id, cross_section)
            self.sections.put(section_id, section)

    def rotMatrix(self,angle):
        cosVal = math.cos(angle)
        sinVal = math.sin(angle)
        return np.array([cosVal, sinVal, 0, 0, 0, 0], [-sinVal, cosVal, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, cosVal, sinVal, 0], [0, 0, 0, -sinVal, cosVal, 0],
                        [0, 0, 0, 0, 0, 1])  # should return the rotational matrix for the element

    def rigidBodyTransMatrix(self,L): #L--> length of the element
        return np.array([[0, 1 / L, 1, 0, -1 / L, 0], [0, 1 / L, 0, 0, -1 / L, 1], [-1, 0, 0, 1, 0, 0]], dtype=float)

    def analyze(self, elementDefINCR,angle,L,K_element,n_sections,tolerance ):  # elementDefIncrement--> 6x1 matrix
        # Pubudu, you code goes here.
        # Get inputs from Imesh as parameters of this function.
        # Get inputs from Me using section.analyze().
        if n_sections==3:
            wh = [1 / 3, 4 / 3, 1 / 3]
            x = [-1 ,0, 1]
        elif n_sections==4:
            wh = [5 / 6 ,1 / 6, 1 / 6, 5 / 6]
            x = [-1, - 0.447214, 0.447214, 1]
        elif n_sections==5:
            wh = [1 / 10, 49 / 90, 32 / 45, 49 / 90, 1 / 10]
            x = [-1, - 0.654654, 0, 0.654654, 1]
        elif n_sections==6:
            wh = [0.066667, 0.378475, 0.554858, 0.554858, 0.378475, 0.066667]
            x = [-1, - 0.765055, - 0.285232, 0.285232, 0.765055, 1]


        rotate=np.matmul(self.rotMatrix(angle),elementDefINCR )
        basicSystem= np.matmul(self.rigidBodyTransMatrix(L),rotate)
        elementForceINCR= np.matmul(K_element,basicSystem)

        # for Section_ in self.sections:
        #     NP = [[0, 0, 1], [(x[section_] + 1) / 2 - 1, (x[section_] + 1) / 2 + 1, 0]]



        for section_ in range(n_sections):
            NP=[[0,0,1],[(x[section_]+1)/2 -1,(x[section_]+1)/2 +1,0]]
            sectionForceINCR= np.matmul(NP,elementForceINCR)

            Section_K=self.sections[section_].analyze([0,0])
            #Section_K=self.cross_section.analyze([0,0]) # send to suneth and get inital section stiffness

            unbalanceForce=tolerance+1000

            while(unbalanceForce>=tolerance):

                sectionDefINCR_ =  np.matmul(np.linalg.inv(Section_K) ,sectionForceINCR)

                cross_section_result=self.cross_section.analyze(sectionDefINCR_)

                sectionResistingForce=cross_section_result[0]

                Section_K = cross_section_result[1]

                unbalanceForce=sectionForceINCR-sectionResistingForce

                sectionForceINCR=unbalanceForce

            self.sections[section_].section_k=Section_K




        elementFlexibMat=None
        for section_ in range(n_sections):
            NP = [[0, 0, 1], [(x[section_] + 1) / 2 - 1, (x[section_] + 1) / 2 + 1, 0]]
            fh= np.linalg.inv(self.sections[section_].section_k)
            mat1=np.matmul(np.transpose(NP),fh)

            elementFlexibMat+=np.matmul(mat1,NP)





















