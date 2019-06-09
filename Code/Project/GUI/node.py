import numpy as np

import gui.tools.find_closest as fc
import pyqtgraph.opengl as gl
from gui.tools.ellipse import EllipseItem

from classes.restraint import Restraint
from classes.loads.point_load import PointLoad


class Node:
    def __init__(self, x, y, z, degree=1, restraint=Restraint(), point_load=None):
        self.x = x
        self.y = y
        self.z = z
        self.restraint = restraint
        if not point_load:
            self.point_load = PointLoad()
        else:
            self.point_load = point_load

        self.degree = degree
        self.is_selected = False

        self.selection_indicator_circle = None
        self.is_selection_indicator_circle_drawn = False

        self.selection_indicator_sphere = None
        self.is_selection_indicator_sphere_drawn = False

        self.load_indicators = None
        self.is_load_indicator_drawn = False

    # def to_string(self):
    #     node_coordinate = "(" + str(self.x) + ", " + str(self.y) + ", " + str(
    #         self.z) + ")"
    #     return node_coordinate
    def paint_in_2d(self, selected_plane, selected_value, max_len_grid, view_2d):
        self.erase_in_2d(view_2d)
        if self.get_plane_value(selected_plane) == selected_value:
            indicator_center = self.get_2d_coordinates(selected_plane)
            rx = max_len_grid / 50
            ry = rx

            self.selection_indicator_circle = EllipseItem(indicator_center, rx, ry)
            view_2d.addItem(self.selection_indicator_circle)
            self.is_selection_indicator_circle_drawn = True

    def paint_in_3d(self, max_len, view_3d):
        self.erase_3d(view_3d)

        selection_indicator_sphere_data = gl.MeshData.sphere(rows=4, cols=4, radius=max_len/50)
        self.selection_indicator_sphere = gl.GLMeshItem(meshdata=selection_indicator_sphere_data, smooth=True,
                                                        drawFaces=False, drawEdges=True, edgeColor=(1, 0, 0, 1))
        self.selection_indicator_sphere.translate(*self.to_list())

        if not self.is_selection_indicator_sphere_drawn:
            view_3d.addItem(self.selection_indicator_sphere)
            self.is_selection_indicator_sphere_drawn = True

    def erase_3d(self, view_3d):
        if self.is_selection_indicator_sphere_drawn:
            view_3d.removeItem(self.selection_indicator_sphere)
            self.is_selection_indicator_sphere_drawn = False

    def erase_in_2d(self, view_2d):
        if self.is_selection_indicator_circle_drawn:
            view_2d.removeItem(self.selection_indicator_circle)
            self.is_selection_indicator_circle_drawn = False

    def paint_node(self, selected_plane, selected_value, max_len_grid, max_len_3d, view_2d, view_3d):
        self.paint_in_2d(selected_plane, selected_value, max_len_grid, view_2d)
        self.paint_in_3d(max_len_3d, view_3d)

    def paint_loads_in_2d(self, selected_plane, selected_value, max_len_grid, f_max, view_2d):
        self.erase_loads_2d(view_2d)
        if self.get_plane_value(selected_plane) == selected_value:
            self.load_indicators = self.point_load.get_visual(self, max_len_grid, f_max, selected_plane)
            for indicator in self.load_indicators:
                if indicator:
                    view_2d.addItem(indicator)
                    self.is_load_indicator_drawn = True

    def erase_loads_2d(self, view_2d):
        if self.is_load_indicator_drawn:
            for indicator in self.load_indicators:
                if indicator:
                    view_2d.removeItem(indicator)
            self.is_load_indicator_drawn = False

    def paint_loads(self, selected_plane, selected_value, max_len_grid, f_max, view_2d, view_3d):
        self.paint_loads_in_2d(selected_plane, selected_value, max_len_grid, f_max, view_2d)

    def select(self):
        self.is_selected = True

    def deselect(self, view_2d, view_3d):
        self.is_selected = False
        self.erase_in_2d(view_2d)
        self.erase_3d(view_3d)

    def get_f_max(self):
        return self.point_load.get_f_max()

    def to_array(self):
        return np.array([self.x, self.y, self.z])

    def to_list(self):
        return [self.x, self.y, self.z]

    def generate_3d_coordinates(self, selected_plane, selected_value, mousePoint, grid_3d):
        if selected_plane == 2:
            node_coords = Node(fc.find_closest(mousePoint.x(), grid_3d.x_coords),
                               fc.find_closest(mousePoint.y(), grid_3d.y_coords),
                               selected_value)

            return node_coords

        elif selected_plane == 1:
            node_coords = Node(fc.find_closest(mousePoint.x(), grid_3d.x_coords), selected_value,
                               fc.find_closest(mousePoint.y(),
                                               grid_3d.z_coords))

            return node_coords

        elif selected_plane == 0:
            node_coords = Node(selected_value, fc.find_closest(mousePoint.x(), grid_3d.y_coords),
                               fc.find_closest(mousePoint.y(),
                                               grid_3d.z_coords))

            return node_coords

    def generate_3d_coordinates_from_point(self, selected_plane, selected_value, point, grid_3d):
        if selected_plane == 2:
            node_coords = Node(fc.find_closest(point[0], grid_3d.x_coords), fc.find_closest(point[1], grid_3d.y_coords),
                               selected_value)

            return node_coords

        elif selected_plane == 1:
            node_coords = Node(fc.find_closest(point[0], grid_3d.x_coords), selected_value,
                               fc.find_closest(point[1], grid_3d.z_coords))

            return node_coords

        elif selected_plane == 0:
            node_coords = Node(selected_value, fc.find_closest(point[0], grid_3d.y_coords),
                               fc.find_closest(point[1], grid_3d.z_coords))

            return node_coords

    def node_exists(self, node_list, change_degree=False):
        for i, node in enumerate(node_list):
            if self == node:
                if change_degree is True:
                    node_list[i].degree += 1
                return True
        # for node in node_list:
        #     if self.x == node.x and self.y == node.y and self.z == node.z:
        #         if change_degree is True:
        #             node.degree += 1
        #         return True

        return False

    def nodes_equal(self, node2):
        if self.x == node2.x and self.y == node2.y and self.z == node2.z:
            return True
        else:
            return False

    def get_plane_value(self, selected_plane):
        if selected_plane == 0:
            return self.x
        elif selected_plane == 1:
            return self.y
        elif selected_plane == 2:
            return self.z

    def get_2d_coordinates(self, selected_plane):
        arr = self.to_array()
        return arr[np.arange(3) != selected_plane]

    def decrease_degree(self, node_list):
        # print(self.to_string(), 'with degree ', self.degree)
        for i, node in enumerate(node_list.nodes_list):
            if node == self:
                if node.degree > 1:
                    node.degree -= 1
                else:
                    node_list.nodes_list.remove(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

