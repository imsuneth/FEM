class Material:

    def __init__(self, id, name, youngs_mod):
        self.id = id
        self.name = name
        self.youngs_mod = youngs_mod

    def getStrainFromStress(self, material_id, stress):
        E = 0;
        if material_id==0:
            fc_dash = -42800;
            ec_dash = -0.002;
            npop = 0.8 + (-fc_dash * 0.001 / 17);
            E = fc_dash * ((npop - 1 + (0 / ec_dash) ^ (npop * 1)) * (npop / ec_dash) - npop * (0 / ec_dash) * (
                    npop * 1 * (0 / ec_dash) ^ (npop * 1 - 1) * (1 / ec_dash))) / (
                        npop - 1 + (0 / ec_dash) ^ (npop * 1)) ^ 2;

        return E
