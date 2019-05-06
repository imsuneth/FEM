# from numpy.linalg import inv
# x=[[1,2],[2,2]]
# x=np.array(x)
# y=[[1,2,3],[4,5,6]]
# y=np.array(y)
# z=np.array([[1,2],[2,2],[3,4]])
# print(x)
# print(y)
# print(z)
# #print(np.matmul(x,y))
# #print(np.dot(x,y))
# print(x@y)
# print(x@y@z)
# #print(inv(x))
# #print(np.dot(x,y))

# numeric_level = getattr(logging, loglevel.upper(), None)
# if not isinstance(numeric_level, int):
#     raise ValueError('Invalid log level: %s' % loglevel)
# logging.basicConfig(level=numeric_level, ...)
import numpy as np
import logging
kLocal = np.ndarray((3, 12,12), dtype=np.float32)
#print(kLocal)
nodes = np.ndarray((4, 3), dtype=np.float32)
#print(nodes)

kGlobal = np.ndarray((4 * 6, 4 * 6))
print(kGlobal)