class DistributedLoad:
    def __init__(self, lx=0, fx=0, ly=0, fy=0, lz=0, fz=0):
        self.lx = float(lx)
        self.fx = float(fx)
        self.ly = float(ly)
        self.fy = float(fy)
        self.lz = float(lz)
        self.fz = float(fz)

    def copy_from_other(self, other):
        self.lx = other.lx
        self.fx = other.fx
        self.ly = other.ly
        self.fy = other.fy
        self.lz = other.lz
        self.fz = other.fz
