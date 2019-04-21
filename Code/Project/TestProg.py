import numpy as np
from numpy.linalg import inv
x=np.array([[1,21,3],[41,5,6],[3,4,2]])
y=np.array([[1,2,3],[4,5,6],[3,2,11]])
z=x@y
print(z)
t=np.matmul(inv(x),z)
print(t)
p=np.zeros((2,1))
print(p)