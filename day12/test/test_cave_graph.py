import unittest

from day12.cave_graph import CaveGraph

class TestCaveGraph(unittest.TestCase):

    def test_constructor_with_duplicate_edges_raises_value_error(self):
        with self.assertRaises(ValueError):
            CaveGraph([("a", "b"), ("a", "b"), ("a", "b")])

    def test_constructor_with_ill_formatted_edges_raises_value_error(self):
        with self.assertRaises(ValueError):
            CaveGraph([("a", "b", "c"), ("b", "d", "a")])

    def test_graphs_are_bidirectional(self):
        self.assertEqual(str(CaveGraph([("a", "b")])), "a-b\nb-a\n")

    def test_start_is_not_bidirectional(self):
        self.assertEqual(str(CaveGraph([("start", "a")])), "start-a\n")

    def test_end_is_not_bidirectional(self):
        self.assertEqual(str(CaveGraph([("a", "end")])), "a-end\n")

    def test_path_start_to_end(self):
        cave = CaveGraph([("start", "end")])
        self.assertSetEqual(set(cave.all_paths()), set(["start,end"]))

    def test_path_linear_small_caves(self):
        cave = CaveGraph([("start", "a"), ("a", "b"), ("b", "c"), ("c", "end")])
        self.assertSetEqual(set(cave.all_paths()), set(["start,a,b,c,end"]))

    def test_path_unreachable_branch(self):
        cave = CaveGraph([("start", "a"), ("a", "b"), ("a", "c"), ("c", "end")])
        self.assertSetEqual(set(cave.all_paths()), set(["start,a,c,end"]))

    def test_path_reachable_branch(self):
        cave = CaveGraph([("start", "A"), ("A", "b"), ("A", "c"), ("c", "end")])
        expected = set([
            "start,A,b,A,c,end",
            "start,A,c,end"
        ])
        self.assertSetEqual(set(cave.all_paths()), expected)

    def test_path_reachable_branch_if_extra_visit(self):
        cave = CaveGraph([("start", "a"), ("a", "b"), ("a", "c"), ("c", "end")])
        expected = set([
            "start,a,c,end",
            "start,a,b,a,c,end"
        ])
        self.assertSetEqual(set(cave.all_paths(extra_visit=True)), expected)
