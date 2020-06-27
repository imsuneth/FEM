from matplotlib import pyplot as plt

from Structure import *
from JsonRead import *
from Material import *

# structure_js = readFile('hipoStructure.json')
structure_js = readFile('testStructure.json')
# structure_js = readFile('structure00.json')
material_models_js = readFile('material_models.json')
load_material_models(material_models_js)
structure = Structure(structure_js)

total_section_deformation = np.array([[0], [0]], dtype=np.float64)
total_section_force = np.array([[0], [0]], dtype=np.float64)

initial_section_k = np.array([[4.01601550e+06, -3.63797881e-11], [-3.63797881e-11, 5.34565486e+04]])


# initial_section_k = np.array([[4.55056806e+06, -2.18278728e-11], [-2.18278728e-11, 9.76568675e+04]])
# initial_section_k = np.array([[5.612190356482407e+06, 0], [0, 0.119102335060676e+06]])


def conditionCheck(mat, value):
    max_abs_val = abs(max(mat.min(), mat.max(), key=abs))
    if max_abs_val > value:
        return True
    else:
        return False


section = structure.elements[0].sections[0]
section.k_section = initial_section_k


def test_section(section_force):
    global total_section_deformation
    global total_section_force

    total_section_force += section_force
    # initial_section_deformation = np.matmul(np.linalg.inv(initial_section_k), section_force)
    # initial_section_deformation = np.matmul(inv(section.k_section), total_section_force) #-->change
    initial_section_deformation = np.matmul(inv(section.k_section), section_force)  # -->change

    total_section_deformation += initial_section_deformation

    section.analyze(total_section_deformation)

    unbalance_force = total_section_force - section.f_section_resist
    iterations = 0

    while conditionCheck(unbalance_force, 0.1):
        corrective_deformation = np.matmul(inv(section.k_section), unbalance_force)

        total_section_deformation += corrective_deformation
        section.analyze(total_section_deformation)
        unbalance_force = total_section_force - section.f_section_resist
        # print('section force\n', total_section_force)
        # print('section_resist\n', section.f_section_resist)
        # print('section stiffness\n', section.k_section)
        print('unbalance_force\n', unbalance_force)
        iterations += 1

        # print('in while loop')
    print('iterations:', iterations)


for y_force in range(0, 1000):
    section_force = np.array([[0], [2]])
    test_section(section_force)
    x_values = total_section_deformation[1]
    y_values = total_section_force[1]

    # print(total_section_force)
    # plt.xlim([0,0.01])

    plt.scatter(x_values, y_values)
    print('total_section_deformation:\n', total_section_deformation, '\ntotal_section_force:\n', total_section_force)

    if (x_values < 0):
        break

    plt.pause(0.01)
    print('\ny_force:', y_force)

plt.show()
