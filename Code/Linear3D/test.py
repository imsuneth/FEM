import numpy as np
a=np.array([[1,2],[2,3]])
b=np.array([[1,2,3,4,5],
			[11,12,13,14,15],
			[21,22,23,24,25],
			[31,32,33,34,35],
			[41,42,43,44,45]])
print("a\n",a)
print("b\n",b)
b[2:4,2:4]=a
print(b)
c=np.zeros((3,4))
print(c)