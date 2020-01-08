from Structure import *
from JsonRead import *
from Material import *
from Main import *
from Structure import *
from matplotlib import pyplot as plt

total_section_deformation = 0
total_section_force = 0
initial_section_k = np.array([[5.78976806e+06, -2.91038305e-11], [-2.91038305e-11, 1.47224867e+05]])


def conditionCheck(mat, value):
    max_abs_val = abs(max(mat.min(), mat.max(), key=abs))
    if max_abs_val > value:
        return True
    else:
        return False


def test_section(section_force):
    global total_section_deformation
    global total_section_force

    initial_section_deformation = np.matmul(np.linalg.inv(initial_section_k), section_force)
    total_section_deformation += initial_section_deformation
    section = structure.elements[0].sections[0]
    section.analyze(total_section_deformation)
    total_section_force += section_force
    unbalanceForce = total_section_force - section.f_section_resist

    while (conditionCheck(unbalanceForce, 0.1)):
        corrective_deformation = np.matmul(inv(section.k_section), unbalanceForce)

        total_section_deformation += corrective_deformation
        section.analyze(total_section_deformation)
        unbalanceForce = total_section_force - section.f_section_resist

        # print('in while loop')


for y_force in range(0, 1000):
    section_force = np.array([[0], [3]])
    test_section(section_force)
    x_values = total_section_deformation[1]
    y_values = total_section_force[1]
    # print(total_section_force)
    # plt.xlim([0,0.01])
    plt.scatter(x_values, y_values)
    plt.pause(0.01)
    print('\ny_force:', y_force)

plt.show()
