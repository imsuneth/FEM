from sympy import *


class Material:
    x = Symbol('x')
    y_concrete = x ** 2 + 1
    y_concrete_prime = y_concrete.diff(x)
    y_steel = x ** 3 + 1
    y_steel_prime = y_steel.diff(x)

    def get_strain_from_stress(self, material_id, stress):

        if material_id == 0:  # concrete
            return self.y_concrete.evalf(subs={self.x: stress})
        elif material_id == 1:  # steel
            return self.y_steel.evalf(subs={self.x: stress})

    def get_e(self, material_id, stress):

        if material_id == 0:  # concrete
            return self.y_concrete_prime.evalf(subs={self.x: stress})
        elif material_id == 1:  # steel
            return self.y_steel_prime.evalf(subs={self.x: stress})
