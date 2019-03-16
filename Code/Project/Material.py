class Material:

    def __init__(self, id, name, youngs_mod):
        self.id = id
        self.name = name
        self.youngs_mod = youngs_mod

    def getStrainFromStress(self, stress):
        return stress * 2.3
