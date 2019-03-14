import numpy as np
import Fiber


class ElementType:
    id = None
    area = None
    fibers = None
    n_fibers = None
    youngs_mod = None
    density = None

    def __init__(self, n_fibers):
        self.fibers = np.array(n_fibers, dtype=Fiber)
        return None


class SquareElementType(ElementType):
    width = None
    height = None

    def __init__(self, width, height, youngs_mod, density):
        self.width = width
        self.height = height


class CircularElementType(ElementType):
    radius = None

    def __init__(self, radius, youngs_mod, density):
        self.radius = radius
