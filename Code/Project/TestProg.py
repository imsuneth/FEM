
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
print("before import")
import math

print("before functionA")
def functionA():
    print("Function A")

print("before functionB")
def functionB():
    print("Function B {}".format(math.sqrt(100)))

print("before __name__ guard")
if __name__ == '__main__':
    functionA()
    functionB()
print("after __name__ guard")