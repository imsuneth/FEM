import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

import gui.local_axes as la
import classes.node as nd

import gui.tools.line_segment as draw_line
from PyQt4 import QtGui
from classes.loads.distributed_load import DistributedLoad


class Element:
    """
    Represents an element

    Contains attributes describing start node, end node, color to be drawn in, whether or not the element is currently
    selected, local axes of the element.
    """
    def __init__(self, start_node, end_node, section=None, color=(0, 0, 128), selected_color=(255, 0, 0),
                 distributed_load=DistributedLoad()):
        if (isinstance(start_node, nd.Node) and isinstance(end_node, nd.Node)) or \
                (start_node is None and end_node is None):
            self.start_node = start_node
            self.end_node = end_node

        else:
            self.start_node = nd.Node(start_node[0], start_node[1], start_node[2])
            self.end_node = nd.Node(end_node[0], end_node[1], end_node[2])

        self.distributed_load = distributed_load
        self.section = section

        self.color_3d = pg.glColor(*color)
        self.color_2d = QtGui.QColor(*color)
        self.current_color_3d = pg.glColor(*color)
        self.current_color_2d = QtGui.QColor(*color)
        self.selected_color_3d = pg.glColor(*selected_color)
        self.selected_color_2d = QtGui.QColor(*selected_color)
        self.width = 2

        self.is_selected = False
        self.is_drawn_in_2d = False
        if self.start_node and self.end_node:
            self.line_in_3d_coords = np.array([[self.start_node.x, self.start_node.y, self.start_node.z],
                                    [self.end_node.x, self.end_node.y, self.end_node.z]])
        else:
            self.line_in_3d_coords = None
        self.drawn_line_in_3d = None
        self.is_drawn_in_3d = False
        self.line_in_2d_coords = False
        self.drawn_line_in_2d = None
        self.local_axes = None

    # def to_string(self):
    #     element_string = "[" + self.start_node.to_string() + ", " + self.end_node.to_string() + "]"
    #     return element_string

    def paint_in_2d(self, selected_plane, selected_value, view_2d):
        self.erase_2d(view_2d)

        self.line_in_2d_coords = self.line_in_3d_coords[:, np.arange(3) != selected_plane]
        self.drawn_line_in_2d = draw_line.LineSegment(self.line_in_2d_coords[0], self.line_in_2d_coords[1],
                                                      self.current_color_2d, self.width)
        if self.line_in_3d_coords[0][selected_plane] == self.line_in_3d_coords[1][selected_plane] == selected_value and\
                not self.is_drawn_in_2d:
            view_2d.addItem(self.drawn_line_in_2d)
            self.is_drawn_in_2d = True
        elif self.is_drawn_in_2d:
            view_2d.removeItem(self.drawn_line_in_2d)
            self.is_drawn_in_2d = False

    def paint_in_3d(self, view_3d):
        self.erase_3d(view_3d)

        self.drawn_line_in_3d = gl.GLLinePlotItem(pos=self.line_in_3d_coords,
                                                  color=self.current_color_3d,
                                                  width=1.5,
                                                  antialias=True)

        if not self.is_drawn_in_3d:
            view_3d.addItem(self.drawn_line_in_3d)
            self.is_drawn_in_3d = True

    def paint_element(self, selected_plane, selected_value, view_2d, view_3d):
        self.paint_in_2d(selected_plane, selected_value, view_2d)
        self.paint_in_3d(view_3d)

    def erase_2d(self, view_2d):
        if self.is_drawn_in_2d:
            view_2d.removeItem(self.drawn_line_in_2d)
            self.is_drawn_in_2d = False

    def erase_3d(self, view_3d):
        if self.is_drawn_in_3d:
            view_3d.removeItem(self.drawn_line_in_3d)
            self.is_drawn_in_3d = False

    def erase_element(self, view_2d, view_3d):
        self.erase_2d(view_2d)
        self.erase_3d(view_3d)

    def distance_from_point_2d(self, mousePoint):
        point = np.array([mousePoint.x(), mousePoint.y()])
        return np.abs(np.cross(self.line_in_2d_coords[1] - self.line_in_2d_coords[0],
                               self.line_in_2d_coords[0] - point)) / \
               np.linalg.norm(self.line_in_2d_coords[1] - self.line_in_2d_coords[0])

    def toggle_selected(self):
        if self.is_selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        self.is_selected = True
        self.current_color_3d = self.selected_color_3d
        self.current_color_2d = self.selected_color_2d
        self.drawn_line_in_3d.setData(color=self.current_color_3d)
        self.drawn_line_in_2d.change_color(self.current_color_2d)

    def deselect(self):
        self.is_selected = False
        self.current_color_3d = self.color_3d
        self.current_color_2d = self.color_2d
        self.drawn_line_in_3d.setData(color=self.current_color_3d)
        self.drawn_line_in_2d.change_color(self.current_color_2d)

    def element_matches(self, line):
        if np.array_equal(self.start_node.to_array(), line[0]) and np.array_equal(self.end_node.to_array(), line[1]):
            return True
        else:
            return False

    def is_same_element(self, element):
        if np.array_equal(self.start_node.to_array(), element.start_node.to_array()) and \
                np.array_equal(self.end_node.to_array(), element.end_node.to_array()):
            return True
        else:
            return False

    def show_local_axes(self, view_3d):
        if self.local_axes is None:
            self.local_axes = la.LocalAxes(self)
            self.local_axes.orient_local_axes()
        self.local_axes.show_local_axes(view_3d)

    def hide_local_axes(self, view_3d):
        self.local_axes.hide_local_axes(view_3d)
        self.local_axes = None

    def get_node_ids(self, node_to_id):
        return node_to_id[self.start_node], node_to_id[self.end_node]

    def __eq__(self, other):
        if isinstance(other, Element):
            self.is_same_element(other)
        else:
            self.element_matches(other)

    def __hash__(self):
        return hash((self.start_node.x, self.start_node.y, self.start_node.z, self.end_node.x, self.end_node.y,
                     self.end_node.z))

    def __repr__(self):
        return '[' + str(self.start_node) + ', ' + str(self.end_node) + ']' + ' - ' + self.section
