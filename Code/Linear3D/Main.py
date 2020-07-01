from Structure import *
from JsonRead import *
import Material

material_js = readFile('material_models.json')
Material.load_material_models(material_js)

# structure_js = readFile('testStructure.json')
# structure_js = readFile('structure00.json')
structure_js = readFile('structure01.json')
structure = Structure(structure_js)
structure.visualize(deformed=False)
input('Press enter to start')
structure.analyzeStructure()
structure.visualize(deformed=True)
input('Press enter to quit')