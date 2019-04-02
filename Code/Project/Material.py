from sympy import *

x = Symbol('x')

y_concrete = x ** 2 + 1
f_concrete = lambdify(x, y_concrete)
y_concrete_prime = y_concrete.diff(x)
f_concrete_prime = lambdify(x, y_concrete_prime)

y_steel = x ** 3 + x +2
f_steel = lambdify(x, y_steel)
y_steel_prime = y_steel.diff(x)
f_steel_prime = lambdify(x, y_steel_prime)


def get_strain_from_stress(material_id, stress):
    if material_id == 0:  # concrete
        return f_concrete(stress)
    elif material_id == 1:  # steel
        return f_steel(stress)


def get_e(material_id, stress):
    if material_id == 0:  # concrete
        return f_concrete_prime(stress)
    elif material_id == 1:  # steel
        return f_steel_prime(stress)