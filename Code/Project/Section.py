import numpy as np
import Fiber


class Section:
    id = None
    area = None
    fibers = None
    n_fibers = None

    def __init__(self, n_fibers):
        self.fibers = np.array(n_fibers, dtype = Fiber)
        return None


class SquareSection(Section):
    width = None
    height = None

    def __init__(self, width, height):
        self.width=width
        self.height=height


class CircularSection(Section):
    radius = None

    def __init__(self, radius):
        self.radius=radius
