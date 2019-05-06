from Structure import *
from JsonRead import *
from CrossSection import *

#from Material import *

structure_js = readFile('testStructure.json')
structure = Structure(structure_js)
#structure.analyzeStructure()


# # Section level test bench----------------------
# section_id = 0
# section_width = 0.2
# section_height = 0.4
# no_of_fibers = 4
# sectional_fiber_material_ids = [0, 1, 0, 0]
#
# cross_section = SquareCrossSection(0, section_width, section_height, no_of_fibers, sectional_fiber_material_ids)
# section = Section(0, cross_section)
#
# section_deformation = [0, 0]  # eps_0, k
# [R, K] = section.analyze(section_deformation)
#
# print("Reaction force: ", R)
# print("Sectional stiffness \n", K)

