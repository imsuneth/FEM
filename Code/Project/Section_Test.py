from Structure import *
from JsonRead import *
from Material import *
from Main import *
from Structure import *
from matplotlib import pyplot as plt

total_section_deformation = np.array([[0], [0]], dtype=np.float64)
total_section_force = np.array([[0], [0]], dtype=np.float64)
initial_section_k = np.array([[4.55056806e+06, -2.18278728e-11], [-2.18278728e-11, 9.76568675e+04]])

def conditionCheck(mat, value):
    max_abs_val = abs(max(mat.min(), mat.max(), key=abs))
    if max_abs_val > value:
        return True
    else:
        return False

section = structure.elements[0].sections[0] #-->change
section.k_section=initial_section_k #-->change

def test_section(section_force):
    global total_section_deformation
    global total_section_force
    total_section_force += section_force
    #initial_section_deformation = np.matmul(np.linalg.inv(initial_section_k), section_force)
    #initial_section_deformation = np.matmul(inv(section.k_section), total_section_force) #-->change
    initial_section_deformation = np.matmul(inv(section.k_section), section_force)  # -->change
    total_section_deformation += initial_section_deformation

    section.analyze(total_section_deformation)

    unbalanceForce = total_section_force - section.f_section_resist
    
    while (conditionCheck(unbalanceForce, 10**(-10))):
        corrective_deformation = np.matmul(inv(section.k_section), unbalanceForce)

        total_section_deformation += corrective_deformation
        section.analyze(total_section_deformation)
        unbalanceForce = total_section_force - section.f_section_resist

        #print('in while loop----------------------------------------')


for y_force in range(0,1000):

    section_force = np.array([[0],[3]])
    test_section(section_force)
    x_values = total_section_deformation[1]
    y_values = total_section_force[1]
    #print(total_section_force)
    #plt.xlim([0,0.01])

    print("call plotting")
    if x_values<0:
        x_values=-1*x_values
    plt.scatter(x_values, y_values)

    plt.pause(0.01)
    print('y_force:',y_force)

plt.show()
