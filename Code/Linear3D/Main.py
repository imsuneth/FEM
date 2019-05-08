from Structure import *
from JsonRead import *

structure_js = readFile('testStructure.json')
structure = Structure(structure_js)
structure.analyzeStructure()


