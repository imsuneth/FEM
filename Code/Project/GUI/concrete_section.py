class ConcreteSection:
    def __init__(self, name, material, section_shape, dimensions):
        self.name = name
        self.material = material
        self.section_shape = section_shape
        self.dimensions = dimensions

    def to_list(self):
        return [
            'Name: ' + self.name + '\n',
            'Material: ' + self.material + '\n',
            'Section Shape: ' + self.section_shape + '\n'
        ] + self.dimensions.dimensions.to_list()
