class ElasticMaterial:
    def __init__(self, name, weight, mass, elasticity, poisson, thermal, shear):
        self.name = name
        self.weight = float(weight)
        self.mass = float(mass)
        self.elasticity = float(elasticity)
        self.poisson = float(poisson)
        self.thermal = float(thermal)
        self.shear = float(shear)

    def to_list(self):
        return ['Name: ' + self.name + '\n',
                'Weight / unit volume: ' + str(self.weight) + '\n',
                'Mass / unit volume: ' + str(self.mass) + '\n',
                'Modulus of Elasticity: ' + str(self.elasticity) + '\n',
                'Poisson\'s Ratio: ' + str(self.poisson) + '\n',
                'Coefficient of Thermal Expansion: ' + str(self.thermal) + '\n',
                'Shear Modulus: ' + str(self.shear)]

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name
