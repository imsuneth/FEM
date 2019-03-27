import numpy as np
# x=[[1,1,0],[2,0,1]]
# #print(x)
# x=np.array(x,dtype=int)
# print(x)
# print(np.transpose(x))
x=np.array([[1,2],[3,4]])
y=np.array([[5,6],[7,8]])
z=np.array([[9,10],[11,12]])
t=np.matmul(y,x)
print(t)
#print(np.matmul(x,y,z))

# print(np.matmul(t,z))
# print(x.dot(y).dot(z))
# print(reduce(np.dot(x,y,z)))