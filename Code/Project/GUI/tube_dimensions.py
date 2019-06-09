from classes.section.dimensions import Dimensions


class TubeDimensions(Dimensions):
    def __init__(self, inner_width, inner_depth, outer_width, outer_depth):
        self.inner_width = float(inner_width)
        self.inner_depth = float(inner_depth)
        self.outer_width = float(outer_width)
        self.outer_depth = float(outer_depth)

    def to_list(self):
        return ['Inner Width: ' + str(self.inner_width) + '\n',
                'Inner Depth: ' + str(self.inner_depth) + '\n',
                'Outer Width: ' + str(self.outer_width) + '\n',
                'Outer Depth: ' + str(self.outer_depth)]