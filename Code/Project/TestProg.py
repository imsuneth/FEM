import numpy as np
from numpy.linalg import inv
x=[[1,2],[2,2]]
x=np.array(x)
y=[[1,2,3],[4,5,6]]
y=np.array(y)
z=np.array([[1,2],[2,2],[3,4]])
print(x)
print(y)
print(z)
#print(np.matmul(x,y))
#print(np.dot(x,y))
print(x@y)
print(x@y@z)
#print(inv(x))
#print(np.dot(x,y))