import math

import numpy as np

from Section import *

class Element:
    K_element_initial=None
    K_element=None
    elementResistingForce=None
    elementUnbalanceForce=None

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



    def rotMatrix(self):
        cosVal = math.cos(self.angle)
        sinVal = math.sin(self.angle)
        return np.array([[cosVal, sinVal, 0, 0, 0, 0], [-sinVal, cosVal, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, cosVal, sinVal, 0], [0, 0, 0, -sinVal, cosVal, 0],
                        [0, 0, 0, 0, 0, 1]])  # should return the rotational matrix for the element

    def rigidBodyTransMatrix(self): #L--> length of the element
        L=self.length
        return np.array([[0, 1 / L, 1, 0, -1 / L, 0], [0, 1 / L, 0, 0, -1 / L, 1], [-1, 0, 0, 1, 0, 0]], dtype=float)

    def calInitialElement_K(self):
        if self.n_sections==3:
            wh = [1 / 3, 4 / 3, 1 / 3]
            x = [-1 ,0, 1]
        elif self.n_sections==4:
            wh = [5 / 6 ,1 / 6, 1 / 6, 5 / 6]
            x = [-1, - 0.447214, 0.447214, 1]
        elif self.n_sections==5:
            wh = [1 / 10, 49 / 90, 32 / 45, 49 / 90, 1 / 10]
            x = [-1, - 0.654654, 0, 0.654654, 1]
        elif self.n_sections==6:
            wh = [0.066667, 0.378475, 0.554858, 0.554858, 0.378475, 0.066667]
            x = [-1, - 0.765055, - 0.285232, 0.285232, 0.765055, 1]

        initialElementFlexibMat=None

        for section_ in range(self.n_sections):
            Section_K = self.sections[section_].analyze([0, 0])
            NP = [[0, 0, 1], [(x[section_] + 1) / 2 - 1, (x[section_] + 1) / 2 + 1, 0]]
            fh = np.linalg.inv(Section_K)
            mat1 = np.matmul(np.transpose(NP), fh)
            initialElementFlexibMat += np.matmul(mat1, NP)

        self.K_element_initial=np.linalg.inv(initialElementFlexibMat)


    def analyze(self,tolerance,initial_call=True):  # for the first iteration set the initial call to True
        # Pubudu, you code goes here.
        # Get inputs from Imesh as parameters of this function.
        # Get inputs from Me using section.analyze().
        elementDefINCR=np.array([[self.start_node.d_y],[self.start_node.d_x],[self.start_node.md_z],[self.end_node.d_y],[self.end_node.d_x],[self.end_node.md_z]])

        if self.n_sections==3:
            wh = [1 / 3, 4 / 3, 1 / 3]
            x = [-1 ,0, 1]
        elif self.n_sections==4:
            wh = [5 / 6 ,1 / 6, 1 / 6, 5 / 6]
            x = [-1, - 0.447214, 0.447214, 1]
        elif self.n_sections==5:
            wh = [1 / 10, 49 / 90, 32 / 45, 49 / 90, 1 / 10]
            x = [-1, - 0.654654, 0, 0.654654, 1]
        elif self.n_sections==6:
            wh = [0.066667, 0.378475, 0.554858, 0.554858, 0.378475, 0.066667]
            x = [-1, - 0.765055, - 0.285232, 0.285232, 0.765055, 1]

        self.calInitialElement_K() # calculate initialElement Stiffness matrix and update K_element_initial

        rotate=np.matmul(self.rotMatrix(self.angle),elementDefINCR )
        basicSystem= np.matmul(self.rigidBodyTransMatrix(self.length),rotate)


        #########################################################################
        if initial_call==True:
            self.K_element=self.K_element_initial
            elementForceINCR= np.matmul(self.K_element,basicSystem)
        else:
            elementForceINCR=self.elementUnbalanceForce-np.matmul(self.K_element,elementDefINCR)
        #########################################################################



        for section_ in range(self.n_sections): # newton raphson iteration
            NP=[[0,0,1],[(x[section_]+1)/2 -1,(x[section_]+1)/2 +1,0]]
            sectionForceINCR= np.matmul(NP,elementForceINCR)

            Section_K=self.sections[section_].analyze([0,0])


            unbalanceForce=tolerance+1000

            while(unbalanceForce>=tolerance):

                sectionDefINCR_ =  np.matmul(np.linalg.inv(Section_K) ,sectionForceINCR)

                cross_section_result=self.cross_section.analyze(sectionDefINCR_)

                sectionResistingForce=cross_section_result[0]

                Section_K = cross_section_result[1]

                unbalanceForce=sectionForceINCR-sectionResistingForce

                sectionForceINCR=unbalanceForce

            self.sections[section_].section_k=Section_K

        elementFlexibMat=None # calculate element stiffness 
        for section_ in range(self.n_sections):
            NP = [[0, 0, 1], [(x[section_] + 1) / 2 - 1, (x[section_] + 1) / 2 + 1, 0]]
            fh= np.linalg.inv(self.sections[section_].section_k)
            mat1=np.matmul(np.transpose(NP),fh)

            elementFlexibMat+=np.matmul(mat1,NP)

        self.K_element=np.linalg.inv(elementFlexibMat)

        self.elementResistingForce=np.matmul(self.K_element,elementDefINCR)

        self.elementUnbalanceForce=elementForceINCR-self.elementResistingForce

        return self.K_element