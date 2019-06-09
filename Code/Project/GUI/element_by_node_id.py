from classes.element import Element


class ElementByNodeId:
    def __init__(self, element: Element, node_to_id):
        self.start_node, self.end_node = element.get_node_ids(node_to_id)
        self.section = element.section
        self.distributed_load = element.distributed_load

