class Restraint:
    def __init__(self, t1_restrained=False, t2_restrained=False, t3_restrained=False,
                 r1_restrained=False, r2_restrained=False, r3_restrained=False):
        self.t1_restrained = t1_restrained
        self.t2_restrained = t2_restrained
        self.t3_restrained = t3_restrained
        self.r1_restrained = r1_restrained
        self.r2_restrained = r2_restrained
        self.r3_restrained = r3_restrained

    def copy_from_other(self, other):
        self.t1_restrained = other.t1_restrained
        self.t2_restrained = other.t2_restrained
        self.t3_restrained = other.t3_restrained
        self.r1_restrained = other.r1_restrained
        self.r2_restrained = other.r2_restrained
        self.r3_restrained = other.r3_restrained
