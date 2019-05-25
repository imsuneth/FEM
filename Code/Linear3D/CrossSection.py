class CrossSection:
    area = 0


class SquareCrossSection(CrossSection):

    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height



    def calculate_inertia(self):
        i_x = self.width * self.height * ((self.width ** 2) + (self.height ** 2)) / 12
        i_y = (self.width * (self.height ** 3)) / 12
        i_z = (self.height * (self.width ** 3)) / 12
        return [i_x, i_y, i_z]


class CircularCrossSection(CrossSection):

    def __init__(self, id, radius):
        self.id = id

        self.radius = radius
