class Fiber:

    def __init__(self, fiber_id, y, width, height, material_id):
        self.id = fiber_id
        self.y = y
        self.width = width
        self.height = height
        self.area = self.height * self.width
        self.material_id = material_id
        self.eps = 0
        self.sigma = 0

