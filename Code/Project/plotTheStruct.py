from matplotlib import pyplot as plt
import numpy as np


def plotTheStruct(elements,nodes):
    plt.ylim(-3, 7)

    for ele in elements:
        startNode = ele.start_node
        endNode = ele.end_node
        x1 = startNode.p_x
        y1 = startNode.p_y

        x2 = endNode.p_x
        y2 = endNode.p_y
        #print(x1, y1, "||", x2, y2)
        plt.plot([x1, x2], [y1, y2], 'r>-')

    for N in nodes:
        x=N.p_x
        y=N.p_y
        ax = plt.axes()
        s="Node "+str(N.id)+"\nFX="+str(round(float(N.f_x.value), 3))+"\nFY="+str(round(float(N.f_y.value), 3))+"\nMZ="+str(round(float(N.m_z.value), 3))
        s+='\nDX=' + str(N.d_x)+'\nDY=' + str(N.d_y)+'\nDMZ=' + str(N.dm_z)
        plt.text(x, y, s)

    plt.show()


