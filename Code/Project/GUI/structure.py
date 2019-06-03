# Last updated - 26/05/2019 #


class Structure:
    """
    Class that represents a structure. Contains:

    - nodes_dict: Dictionary of Node objects (id: Node)
    - elements_dict: Dictionary of ElementByNodeId objects (id: ElementByNodeId)
    - elastic_materials_dict: Dictionary of elastic materials (material_name: ElasticMaterial)
    - concrete_sections_dict: Dictionary of concrete sections (section_name: ConcreteSection)

        - Node class:
            Attributes of Node:
                x (float): x coordinate in global coordinates
                y (float): y coordinate in global coordinates
                z (float): z coordinate in global coordinates
                restraint (Restraint): Object of class Restraint that contains the restraints placed on a Node
                point_load (PointLoad): Object of class PointLoad that represents the point load on a Node

            Methods:
                to_array(): Returns a numpy array [x, y, z]
                to_list(): Returns a list [x, y, z]
                __eq__(other): Overridden to return True if all three coordinates match
                __repr__(): Overridden to return a string "(x, y, z)

        - Restraint class:
            Attributes of Restraint:
                t1 (bool): True if restrained
                t2 (bool): True if restrained
                t3 (bool): True if restrained
                r1 (bool): True if restrained
                r2 (bool): True if restrained
                r3 (bool): True if restrained

        - PointLoad class:
            Attributes of PointLoad:
                fx (float): Load along global x direction
                fy (float): Load along global y direction
                fz (float): Load along global z direction
                mx (float): Moment about global x axis
                my (float): Moment about global y axis
                mz (float): Moment about global z axis

            Methods:
                is_loaded(): Returns True if any load is applied to the node. (Note: Moments are ignored)

        - ElementByNodeId class:
            Attributes of ElementByNodeId:
                start_node (int): Key of starting node in nodes_dict
                end_node (int): Key of ending node in nodes_dict
                section (str): Name of the element's section used to get section properties from concrete_sections_dict
                distributed_load (DistributedLoad): Object of class DistributedLoad that represents the distributed load
                                                    applied on the element.

        - ConcreteSection class:
            Attributes of ConcreteSection:
                name (str): Name of concrete section
                material (ElasticMaterial): Object of class ElasticMaterial that contains the material properties
                section_shape (str): Name of section shape (Can be rectangular, circular, pipe, or tube as of now)
                dimensions (Dimensions): An object of class RectangularDimensions, CircularDimensions, PipeDimensions,
                                         or TubeDimensions depending on the shape of the section.

        - ElasticMaterial class:
            Attributes of ElasticMaterial:
                name (str)
                weight (float)
                mass (float)
                elasticity (float)
                poisson (float)
                thermal (float)
                shear (float)

        RectangularDimensions class:
            Attributes of RectangularDimensions:
                width (float)
                depth (float)

        CircularDimensions class:
            Attributes of CircularDimensions:
                radius (float)

        PipeDimensions class:
            Attributes of PipeDimensions:
                inner_radius (float)
                outer_radius (float)

        TubeDimensions class:
            Attributes of TubeDimensions:
                inner_depth (float)
                outer_depth (float)
                inner_width (float)
                outer_width (float)

        DistributedLoad class:
            Attributes of DistributedLoad:
                lx (float): Distance along which maximum load is applied
                ly (float): Distance along which maximum load is applied
                lz (float): Distance along which maximum load is applied
                fx (float): Maximum load
                fy (float): Maximum load
                fz (float): Maximum load



    """
    def __init__(self, fea):
        self.nodes_dict = fea.nodes_list.get_dict()
        self.elements_dict = fea.element_list.get_elements_in_node_ids(self.nodes_dict)
        self.elastic_materials_dict = fea.elastic_material_dict
        self.concrete_sections_dict = fea.concrete_section_dict
