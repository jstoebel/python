import pytest
import pytest_check as check

from pov import (
    Tree, NodeNotFound, traverse
)



# Tests adapted from `problem-specifications//canonical-data.json`

def test_find():
    grandchild = Tree("c")
    child = Tree("b", children=[grandchild])
    tree = Tree("a", children=[child])

    check.equal(tree.find("b"), child)
    check.equal(tree.find("c"), grandchild)

    with pytest.raises(NodeNotFound):
        tree.find("d")
    
class TestFromPov:

    def traverse(self, root):
        return self.traverse_util(root)

    def traverse_util(self, root):
        my_data = [root.label]
        for child in root.children:
            my_data += self.traverse_util(child)
        return my_data

    def assert_tree_equals(self, tree_a, tree_b):
        assert traverse(tree_a) == traverse(tree_b)

    def test_results_in_the_same_tree_if_the_input_tree_is_a_singleton(self):
        tree = Tree("x")
        expected = Tree("x")
        self.assert_tree_equals(tree.from_pov("x"), expected)

    def test_can_reroot_a_tree_with_a_parent_and_one_sibling(self):
        tree = Tree("parent", [Tree("x"), Tree("sibling")])
        expected = Tree("x", [Tree("parent", [Tree("sibling")])])
        self.assert_tree_equals(tree.from_pov("x"), expected)

    def test_can_reroot_a_tree_with_a_parent_and_many_siblings(self):
        tree = Tree("parent", [Tree("a"), Tree("x"), Tree("b"), Tree("c")])
        expected = Tree("x", [Tree("parent", [Tree("a"), Tree("b"), Tree("c")])])
        self.assert_tree_equals(tree.from_pov("x"), expected)

    def test_can_reroot_a_tree_with_new_root_deeply_nested_in_tree(self):
        tree = Tree(
            "level-0",
            [Tree("level-1", [Tree("level-2", [Tree("level-3", [Tree("x")])])])],
        )
        expected = Tree(
            "x",
            [Tree("level-3", [Tree("level-2", [Tree("level-1", [Tree("level-0")])])])],
        )
        self.assert_tree_equals(tree.from_pov("x"), expected)

    def test_moves_children_of_the_new_root_to_same_level_as_former_parent(self):
        tree = Tree("parent", [Tree("x", [Tree("kid-0"), Tree("kid-1")])])
        expected = Tree("x", [Tree("kid-0"), Tree("kid-1"), Tree("parent")])
        self.assert_tree_equals(tree.from_pov("x"), expected)

    def test_can_reroot_a_complex_tree_with_cousins(self):
        tree = Tree(
            "grandparent",
            [
                Tree(
                    "parent",
                    [
                        Tree("x", [Tree("kid-0"), Tree("kid-1")]),
                        Tree("sibling-0"),
                        Tree("sibling-1"),
                    ],
                ),
                Tree("uncle", [Tree("cousin-0"), Tree("cousin-1")]),
            ],
        )
        expected = Tree(
            "x",
            [
                Tree("kid-1"),
                Tree("kid-0"),
                Tree(
                    "parent",
                    [
                        Tree("sibling-0"),
                        Tree("sibling-1"),
                        Tree(
                            "grandparent",
                            [Tree("uncle", [Tree("cousin-0"), Tree("cousin-1")])],
                        ),
                    ],
                ),
            ],
        )
        self.assert_tree_equals(tree.from_pov("x"), expected)

    def test_errors_if_target_does_not_exist_in_a_singleton_tree(self):
        tree = Tree("x")
        with self.assertRaisesWithMessage(ValueError):
            tree.from_pov("nonexistent")

    def test_errors_if_target_does_not_exist_in_a_large_tree(self):
        tree = Tree(
            "parent",
            [
                Tree("x", [Tree("kid-0"), Tree("kid-1")]),
                Tree("sibling-0"),
                Tree("sibling-1"),
            ],
        )
        with self.assertRaisesWithMessage(ValueError):
            tree.from_pov("nonexistent")


class TestPathTo:

    def test_can_find_path_to_parent(self):
        tree = Tree("parent", [Tree("x"), Tree("sibling")])
        expected = ["x", "parent"]
        self.assertEqual(tree.path_to("x", "parent"), expected)

    def test_can_find_path_to_sibling(self):
        tree = Tree("parent", [Tree("a"), Tree("x"), Tree("b"), Tree("c")])
        expected = ["x", "parent", "b"]
        self.assertEqual(tree.path_to("x", "b"), expected)

    def test_can_find_path_to_cousin(self):
        tree = Tree(
            "grandparent",
            [
                Tree(
                    "parent",
                    [
                        Tree("x", [Tree("kid-0"), Tree("kid-1")]),
                        Tree("sibling-0"),
                        Tree("sibling-1"),
                    ],
                ),
                Tree("uncle", [Tree("cousin-0"), Tree("cousin-1")]),
            ],
        )
        expected = ["x", "parent", "grandparent", "uncle", "cousin-1"]
        self.assertEqual(tree.path_to("x", "cousin-1"), expected)

    def test_can_find_path_not_involving_root(self):
        tree = Tree(
            "grandparent",
            [Tree("parent", [Tree("x"), Tree("sibling-0"), Tree("sibling-1")])],
        )
        expected = ["x", "parent", "sibling-1"]
        self.assertEqual(tree.path_to("x", "sibling-1"), expected)

    def test_can_find_path_from_nodes_other_than_x(self):
        tree = Tree("parent", [Tree("a"), Tree("x"), Tree("b"), Tree("c")])
        expected = ["a", "parent", "c"]
        self.assertEqual(tree.path_to("a", "c"), expected)

    def test_errors_if_destination_does_not_exist(self):
        tree = Tree(
            "parent",
            [
                Tree("x", [Tree("kid-0"), Tree("kid-1")]),
                Tree("sibling-0"),
                Tree("sibling-1"),
            ],
        )
        with self.assertRaisesWithMessage(ValueError):
            tree.path_to("x", "nonexistent")

    def test_errors_if_source_does_not_exist(self):
        tree = Tree(
            "parent",
            [
                Tree("x", [Tree("kid-0"), Tree("kid-1")]),
                Tree("sibling-0"),
                Tree("sibling-1"),
            ],
        )
        with self.assertRaisesWithMessage(ValueError):
            tree.path_to("nonexistent", "x")

    # Utility functions
    def assertRaisesWithMessage(self, exception):
        return self.assertRaisesRegex(exception, r".+")


if __name__ == "__main__":
    unittest.main()
