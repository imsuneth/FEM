import unittest
from Structure import *
from JsonRead import readFile
from Material import load_material_models
import numpy as np
import numpy.testing as nptest


class UnitTest(unittest.TestCase):

    # Load the structure for testing
    material_models_js = readFile('.\\materials\\material_models.json')
    load_material_models(material_models_js)
    structure_js = readFile('.\\structures\\testStructure.json')
    structure = Structure(structure_js)

    def test_section(self):
        element0 = self.structure.elements[0]
        section0 = element0.sections[0]
        section0.analyze([0, 0])

        expected = np.round(np.array([
            [4.55056806e+06, -2.18278728e-11],
            [-2.18278728e-11, 9.76568675e+04]]), decimals=2)

        actual = np.round(section0.k_section, decimals=2)
        nptest.assert_array_equal(
            expected, actual, 'Section stiffness miscalculation')

    def test_element(self):
        element0 = self.structure.elements[0]
        k = element0.calInitialElement_K()
        actual = np.round(element0.analyze(0.1), decimals=1)

        expected = np.round(np.array([
            [1.30016230e+06, 7.66579609e-28, -6.23653510e-12, -
                1.30016230e+06, -7.66579609e-28,  6.23653510e-12],
            [-6.05845175e-28, 2.73325103e+04,  4.78318929e+04,
                6.05845175e-28, -2.73325103e+04,  4.78318929e+04],
            [-6.23653510e-12,  4.78318929e+04,  1.11607775e+05,
                6.23653510e-12, -4.78318929e+04,  5.58038505e+04],
            [-1.30016230e+06, -7.66579609e-28,  6.23653510e-12,
                1.30016230e+06, 7.66579609e-28, -6.23653510e-12],
            [6.05845175e-28, -2.73325103e+04, -4.78318929e+04, -
                6.05845175e-28, 2.73325103e+04, -4.78318929e+04],
            [6.23653510e-12,  4.78318929e+04,  5.58038505e+04,  -6.23653510e-12, -4.78318929e+04,  1.11607775e+05]]), decimals=1)

        nptest.assert_array_equal(
            expected, actual, 'Element stiffness miscalculation')


if __name__ == '__main__':
    unittest.main()
