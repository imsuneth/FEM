import numpy as np
import math
from Section  import *
from Element import *

def rigidBodyTransMatrix(L):  # should return rigid body transformation matrix (L--> length of the element)
    return np.array([[0, 1 / L, 1, 0, -1 / L, 0], [0, 1 / L, 0, 0, -1 / L, 1], [-1, 0, 0, 1, 0, 0]], dtype=float)


def rotMatrix(angle):  # return element nodal deformations refering local coordinate system
    cosVal = math.cos(angle)
    sinVal = math.sin(angle)
    return np.array([cosVal, sinVal, 0, 0, 0, 0], [-sinVal, cosVal, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, cosVal, sinVal, 0], [0, 0, 0, -sinVal, cosVal, 0],
                    [0, 0, 0, 0, 0, 1])  # should return the rotational matrix for the element

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



#-----------------------------------------------------------------------------
#assuming there is a object array for sections and elements
elementsObjectArray=[]
sectionsObjectArry=[]
#------------------------------------------------------------------------------

def iteration(elementObj,updatedStrain,numOfItrPoint):
    delta_e=np.dot(rotMatrix(elementObj.angle)*updatedStrain) # deformation increment refering local coordinate system
    delta_e=np.dot(rigidBodyTransMatrix(elementObj.lenght)*delta_e) # transform to basic system

    elementForceIncrement=None # element force increment (what is the matrix should multiply)

    for _ in numOfItrPoint:
        delta_f_section=np.dot(shapeFunction()*elementForceIncrement)
        #**** iteration************


