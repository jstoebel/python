from json import dumps
from typing import List, TypeVar, Optional, Generic

class NodeNotFound(Exception):
    pass

TreeType = TypeVar('TreeType')
class Tree(Generic[TreeType]):
    def __init__(self, label: str, children: List["Tree[TreeType]"]=[]):
        self.label = label
        self.children = children
        self._parent = None

        for child in self.children:
            child.parent = self

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

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def relations(self):
        """
        return all relations (children and parent if any)
        """
        ret_val = self.children[:]
        if self.parent:
            ret_val.append(self.parent)

        return ret_val

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

        starting_node = self.find(from_node)

        return get_path_to(starting_node, to_node, [])

    def find(self, target_node_label: str, caller: "Tree[TreeType]" = None) -> "Tree[TreeType]":
        """
        :param node: label of node to find
        :returns: node or raises NodeNotFound if not found
        """

        for node in self.relations:
            if caller and node.label == caller.label:
                continue
            if node.label == target_node_label:
                return node
            return node.find(target_node_label, self)

        raise NodeNotFound

def traverse(root):
    return traverse_util(root)


def traverse_util(root):
    my_data = [root.label]
    for child in root.children:
        my_data += traverse_util(child)
    return my_data

def get_path_to(node: Tree, target: str, working_path: List[str]) -> List[str]:
    # ask all relations if they can make a path.
    for relation in node.relations:
        # don't ask node if its latest in path (that would be doubling back)
        if relation.label == working_path[-1]:
            # asking this relation would be doubling back. don't
            continue

        new_path = [*working_path, node.label]
        if relation.label == target:
            return new_path

        relation_response = get_path_to(relation, target, new_path)
        if relation_response:
            return relation_response

    # base case of leaf nodes will always get here.