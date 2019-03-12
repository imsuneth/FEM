import numpy as np
import math
from Section import *




def sin(x):
    return math.sin(x)


def cos(x):
    return math.cos(x)


def calLocalStrains(updatedStrain):  # calculating local strains for global strains got from up
    return np.dot(rotMatrix * updatedStrain)


def removeBC_(removeBC):
    return np.dot(removeBC * calLocalStrains())


def rotMatrix(angle):  # return element nodal deformations refering local coordinate system
    cosVal = math.cos(angle)
    sinVal = math.sin(angle)
    return np.array([cosVal, sinVal, 0, 0, 0, 0], [-sinVal, cosVal, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, cosVal, sinVal, 0], [0, 0, 0, -sinVal, cosVal, 0],
                    [0, 0, 0, 0, 0, 1])  # should return the rotational matrix for the element


def rigidBodyTransMatrix(L):  # should return rigid body transformation matrix
    return np.array([[0, 1 / L, 1, 0, -1 / L, 0], [0, 1 / L, 0, 0, -1 / L, 1], [-1, 0, 0, 1, 0, 0]], dtype=float)


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
