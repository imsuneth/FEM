from Structure import *
from JsonRead import *
from Material import *

material_models_js = readFile('.\\materials\\material_models.json')
load_material_models(material_models_js)

# structure_js = readFile('.\\structures\\testStructure.json')
structure_js = readFile('.\\structures\\hipoStructure.json')

structure = Structure(structure_js)
structure.visualize()
# structure.analyze_structure()
