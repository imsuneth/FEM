import numpy as np
import math
from Section import *
from Element import *


def rigidBodyTransMatrix(L):  # should return rigid body transformation matrix (L--> length of the element)
    return np.array([[0, 1 / L, 1, 0, -1 / L, 0], [0, 1 / L, 0, 0, -1 / L, 1], [-1, 0, 0, 1, 0, 0]], dtype=float)


def rotMatrix(angle):  # return element nodal deformations refering local coordinate system
    cosVal = math.cos(angle)
    sinVal = math.sin(angle)
    return np.array([cosVal, sinVal, 0, 0, 0, 0], [-sinVal, cosVal, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, cosVal, sinVal, 0], [0, 0, 0, -sinVal, cosVal, 0],
                    [0, 0, 0, 0, 0, 1])  # should return the rotational matrix for the element


def getElement_k():  # returns the element stiffness matrix
    return


def shapeFunction():
    return None


def forceInterpolationMatrix():  # shold retrun force interpolation function to each section
    return None


def sectionFoceIncrement():
    return None


def sectionStateDeformation():
    return None


def getUpdatedElemntStiffness():
    return None


def getUpdatedElemntStiffnessGlobal():
    return None


# -----------------------------------------------------------------------------
# assuming there is a object array for sections and elements
elementsObjectArray = []
sectionsObjectArry = []


# ------------------------------------------------------------------------------

def calculateResForce():
    pass


def calSection_k():
    pass


def iteration(elementObj, updatedStrain, numOfItrPoint, maxNumOfItr):
    delta_e = np.dot(
        rotMatrix(elementObj.angle) * updatedStrain)  # deformation increment refering local coordinate system
    delta_e = np.dot(rigidBodyTransMatrix(elementObj.lenght) * delta_e)  # transform to basic system

    elementForceIncrement = np.dot(
        getElement_k() * delta_e)  # element force increment (what is the matrix should multiply)

    for _ in numOfItrPoint:
        delta_f_section = np.dot(shapeFunction() * elementForceIncrement)


        for itr in maxNumOfItr:
              # calculate section stiffness
            # res_f=calculateResForce()#calculate_resisting force
            # #newForce=calNewForce()
            # #check the tolerance
            if(checkCovergence()==True):
                break
            else:
                #delta_e_section=section_kInverse(e)*delta_f_section
                # updatedSection_k = calSection_k(delta_e_section)
                # resistingForce= calResistingF()
                # updated_force=
                # delta_e_section=section_kInverse(e_update)*updated_force

            
