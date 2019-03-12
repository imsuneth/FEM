import numpy as np
import Fiber
import sys

class Section:
    id = None
    area = None
    fibers = None
    n_fibers = None

    def __init__(self, n_fibers):
        self.fibers = np.array(n_fibers, dtype = Fiber)
        return None


class SquareSection(Section):
    width = None
    height = None


    def __init__(self, width, height):
        self.width=width
        self.height=height


class CircularSection(Section):
    radius = None

    def __init__(self, radius):
        self.radius=radius
'''
obj1=CircularSection(3)
obj2=CircularSection(4)
print("size of the object1 is ",sys.getsizeof(obj1))
a=np.array([],dtype=CircularSection)
print("size of empty numpy array is ",sys.getsizeof(a))
a=np.append(obj1,a)
a=np.append(obj2,a)
print(sys.getsizeof(a))
b=[]
print("size of the empty list is",sys.getsizeof(b))
b.append(obj1)
b.append(obj2)
print(sys.getsizeof(b))
'''
a=np.arange(10)
b=[0,1,2,3,4,5,6,7,8,9]
print("np ar",sys.getsizeof(a),"list",sys.getsizeof(b),sys.getsizeof(a[1]),sys.getsizeof(51))
print(a[1])