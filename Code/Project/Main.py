from Structure import *
from JsonRead import readFile
from Material import load_material_models

def main():
    material_models_js = readFile('.\\materials\\material_models.json')
    load_material_models(material_models_js)

    # structure_js = readFile('.\\structures\\testStructure.json')
    # structure_js = readFile('.\\structures\\testStructure2.json')
    structure_js = readFile('.\\structures\\hipoStructure.json')

    structure = Structure(structure_js)
    structure.visualize()
    structure.analyze_structure()


if __name__ == "__main__":
    main()