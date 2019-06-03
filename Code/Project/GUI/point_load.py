from PyQt4 import QtGui
from gui.tools.point_load_arrow import PointLoadArrow
import math


class PointLoad:
    def __init__(self, fx=0, fy=0, fz=0, mx=0, my=0, mz=0):
        self.fx = float(fx)
        self.fy = float(fy)
        self.fz = float(fz)
        self.mx = float(mx)
        self.my = float(my)
        self.mz = float(mz)

    def copy_from_other(self, other):
        self.fx = other.fx
        self.fy = other.fy
        self.fz = other.fz
        self.mx = other.mx
        self.my = other.my
        self.mz = other.mz

    def is_loaded(self):
        if self.fx != 0 or self.fy != 0 or self.fz != 0:
            return True
        else:
            return False

    def is_in_plane(self, selected_plane):
        if selected_plane == 0:
            return self.fx == 0
        if selected_plane == 1:
            return self.fy == 0
        if selected_plane == 2:
            return self.fz == 0

    def get_visual(self, node, max_len_grid, f_max, selected_plane):
        l = max_len_grid / 10
        lx = (self.fx / f_max) * l
        ly = (self.fy / f_max) * l
        lz = (self.fz / f_max) * l

        if selected_plane == 2:
            fx_indicator = None
            fy_indicator = None
            if self.fx != 0:
                end_point = [node.x, node.y]
                start_point = [node.x - lx, node.y]
                fx_indicator = PointLoadArrow(start_point, end_point, self.fx, QtGui.QColor(255, 255, 0))
            if self.fy != 0:
                start_point = [node.x, node.y]
                end_point = [node.x, node.y + ly]
                fy_indicator = PointLoadArrow(start_point, end_point, self.fy, QtGui.QColor(255, 255, 0))
            return [fx_indicator, fy_indicator]
        
        elif selected_plane == 1:
            fx_indicator = None
            fz_indicator = None
            if self.fx != 0:
                end_point = [node.x, node.z]
                start_point = [node.x - lx, node.z]
                fx_indicator = PointLoadArrow(start_point, end_point, self.fx, QtGui.QColor(255, 255, 0))
            if self.fz != 0:
                start_point = [node.x, node.z]
                end_point = [node.x, node.z + lz]
                fz_indicator = PointLoadArrow(start_point, end_point, self.fy, QtGui.QColor(255, 255, 0))
            return [fx_indicator, fz_indicator]

        elif selected_plane == 0:
            fy_indicator = None
            fz_indicator = None
            if self.fy != 0:
                end_point = [node.y, node.z]
                start_point = [node.y - ly, node.z]
                fy_indicator = PointLoadArrow(start_point, end_point, self.fy, QtGui.QColor(255, 255, 0))
            if self.fz != 0:
                start_point = [node.y, node.z]
                end_point = [node.y, node.z + lz]
                fz_indicator = PointLoadArrow(start_point, end_point, self.fz, QtGui.QColor(255, 255, 0))
            return [fy_indicator, fz_indicator]

    def get_f_max(self):
        return max(abs(self.fx), abs(self.fy), abs(self.fz))
