from json import dumps
from typing import List, TypeVar, Optional, Generic

class NodeNotFound(Exception):
    pass

TreeType = TypeVar('TreeType')
class Tree(Generic[TreeType]):
    def __init__(self, label: str, children: List["Tree[TreeType]"]=[]):
        self.label = label
        self.children = children

    def __dict__(self):
        return {self.label: [c.__dict__() for c in sorted(self.children)]}

    def __str__(self, indent=None):
        return dumps(self.__dict__(), indent=indent)

    def __lt__(self, other):
        return self.label < other.label

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()

    def __repr__(self):
        return f"<Tree '{self.label}'>"


    def from_pov(self, from_node: str):
        """
        :param from_node: label of node to re-root
        """
        # find node
        # that node becomes root
        # for each relation (up or down):
            # make a child
            # repeat
        pass

    def path_to(self, from_node: str, to_node: str):
        """
        :param from_node: label of node to start from
        :param to_node: label of node to go to
        :returns: ???
        """
        pass

    def find(self, target_node_label: str) -> "Tree[TreeType]":
        """
        :param node: label of node to find
        :returns: node or raises NodeNotFound if not found
        """

        for node in self.children:
            if node.label == target_node_label:
                return node
            return node.find(target_node_label)

        raise NodeNotFound

def traverse(root):
    return traverse_util(root)


def traverse_util(root):
    my_data = [root.label]
    for child in root.children:
        my_data += traverse_util(child)
    return my_data
