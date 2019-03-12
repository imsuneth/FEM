import numpy as np

L = np.array([2, 1, 2])
BC = np.array([1, 2, 3, 10, 11, 12])
Load_applied_dof = 4
Load_vector = np.array([[0], [0], [0], [1], [0], [0], [0], [0], [0], [0], [0], [0]])
noe = 3  # number of elements
ndofpn = 3  # number of degrees of freedoms per node
nonpe = 2  # number of nodes per element
tdof = 12  # total dof
ECM = np.array([[1, 2, 3], [2, 3, 4]])
angle = np.arange(-np.pi, np.pi + 1, np.pi, dtype=float)
nIP = 6  # number of integration points

if nIP == 3:
    wh = [1 / 3, 4 / 3, 1 / 3]
    wh = np.array(wh)
    x = np.array([-1, 0, 1])
elif nIP == 4:
    wh = np.array([5 / 6, 1 / 6, 1 / 6, 5 / 6])
    x = np.array([-1, -0.447214, 0.447214, 1])
elif nIP == 5:
    wh = np.array([1 / 10, 49 / 90, 32 / 45, 49 / 90, 1 / 10])
    x = np.array([-1, -0.654654, 0, 0.654654, 1])
elif nIP == 6:
    wh = np.array([0.066667, 0.378475, 0.554858, 0.554858, 0.378475, 0.066667])
    x = np.array([-1, -0.765055, -0.285232, 0.285232, 0.765055, 1])

width = 0.4  # width of beam in m
d = 0.4  # depth of beam in m
I = (d ** 3) * width / 12  # Second moment of area about centeroidal axis
A = d * width  # cross sectional area

nof = 20  # number of fibers in y direction
nofx = 20  # number of fibers in x direction

Afib = (width / nofx) * (d / nof)  # Area of a fiber

# =================DATA FOR ITERATIONS===============================
displacement_step=0.00001 #Displacement increment in m (Put with the sign)
displacement_steps=50000
max_i=100
max_z=1000

# ....Newton raphson convergence criteria....
tol_force_i=10**(-5)
tol_Energy_i=10**(-3)

#....Section level convergence criteria.....
tol_force_z=10^(-10)


#%===============MATERIAL MODELS=======================

#%...........unconfined concrete properties..........
elements = js["elements"]