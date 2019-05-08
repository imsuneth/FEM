import numpy as np


class MaterialModel:
    def __init__(self, id, name, youngs_mod):
        self.id = id
        self.name = name
        self.youngs_m =youngs_mod
        self.mu = 0.3
        self.g = youngs_mod/2/(1+self.mu)

    def get_e(self):
        return self.youngs_m

    def get_mu(self):
        return self.mu


def load_material_models(js):
    global material_models
    no_of_material_models = js["no_of_material_models"]
    material_models = np.empty(no_of_material_models, dtype=MaterialModel)
    material_models_js = js["material_models"]
    for material_model_js in material_models_js:
        id = material_model_js["id"]
        name = material_model_js["name"]
        youngs_mod = material_models_js["youngs_mod"]
        material_model = MaterialModel(id, name, youngs_mod)
        material_models.put(id, material_model)
