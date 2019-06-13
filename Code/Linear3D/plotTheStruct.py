from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

plot_x_values,plot_y_values,plot_z_values=[],[],[]

def create_list(x,y,z):
    plot_x_values.append(x)
    plot_y_values.append(y)
    plot_z_values.append(z)

def plotNew(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = np.array([z])
    ax.plot_wireframe(x, y, z)
    plt.show()



