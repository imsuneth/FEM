import numpy as np
from numpy import linalg
import math
x=np.array([2,2])
y=np.array([2,0])
z=np.inner(x,y)
print(z)
theta=math.acos(z/(np.linalg.norm(x)*np.linalg.norm(y)))
deg=(180/np.pi)*theta
print(deg)