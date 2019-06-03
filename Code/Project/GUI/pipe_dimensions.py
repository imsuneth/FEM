from classes.section.dimensions import Dimensions


class PipeDimensions(Dimensions):
    def __init__(self, inner_radius, outer_radius):
        self.inner_radius = float(inner_radius)
        self.outer_radius = float(outer_radius)

    def to_list(self):
        return ['Inner Radius: ' + str(self.inner_radius) + '\n',
                'Outer Radius: ' + str(self.outer_radius)]
