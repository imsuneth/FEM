from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = [0,2,3,4,5,6,7,8,9,10],[0,6,2,3,13,4,1,2,4,8],[0,3,3,3,5,7,9,11,9,10]
Z=np.array([Z])
ax.plot_wireframe(X, Y, Z)

plt.show()