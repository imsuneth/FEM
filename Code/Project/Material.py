from sympy import *
import numpy as np
import sys


class MaterialModel:
    def __init__(self, id, no_of_ranges, range_upper_limits, formulas_list):
        self.no_of_ranges = no_of_ranges
        self.id = id
        self.ranges = np.array(range_upper_limits)
        self.formulas = np.empty(no_of_ranges, dtype=Function)
        self.d_formulas = np.empty(no_of_ranges, dtype=Function)
        index = 0
        for formula in formulas_list:
            sympy_formula = sympify(formula)
            f_sympy_formula = lambdify(x, sympy_formula)
            self.formulas.put(index, f_sympy_formula)
            d_sympy_formula = sympy_formula.diff(Symbol('x'))
            f_d_sympy_formula = lambdify(x, d_sympy_formula)
            self.d_formulas.put(index, f_d_sympy_formula)
            index += 1

    def get_strain(self, stress):
        for index in range(self.no_of_ranges):
            if stress < self.ranges[index]:
                return self.formulas[index](stress)

    def get_e(self, stress):
        for index in range(self.no_of_ranges):
            if stress < self.ranges[index]:
                #return self.d_formulas[index](stress)
                return 20*(10**6)


x = Symbol('x')


def load_material_models(js):
    global material_models
    no_of_material_models = js["no_of_material_models"]
    material_models = np.empty(no_of_material_models, dtype=MaterialModel)
    material_models_js = js["material_models"]
    for material_model_js in material_models_js:
        id = material_model_js["id"]
        name = material_model_js["name"]
        no_of_ranges = material_model_js["no_of_ranges"]
        range_upper_limits = material_model_js["range_upper_limits"]
        range_upper_limits.append(sys.float_info.max)
        formulas = material_model_js["formulas"]
        material_model = MaterialModel(id, no_of_ranges, range_upper_limits, formulas)
        material_models.put(id, material_model)