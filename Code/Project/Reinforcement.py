class Reinforcement:
    def __init__(self, material_id, distance_from_centroid, area):
        self.material_id =material_id
        self.distance_from_centroid = distance_from_centroid
        self.area = area
        self.eps = 0
        self.sigma = 0