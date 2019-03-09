from enum import Enum

class MaterialModel(Enum):

    CONCRETE = 0
    STEEL = 1

    young_modulus = {
        CONCRETE:100,
        STEEL:200
    }

    def getYoungModulus(self, material_type):
        return self.young_modulus[material_type]

    def getStrainFromStress(self, stress, material_type):
        if material_type == self.CONCRETE:
            return stress*2.3
        elif material_type == self.STEEL:
            return stress*3.4


