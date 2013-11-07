import unittest
import networkx as nx
from analyze_graph import squelch


class SquelchTest(unittest.TestCase):
    def setUp(self):
        self.g = g = nx.Graph()
        g.add_edge('a', 'b', weight=100)
        g.add_edge('b', 'c', weight=50)
        g.add_edge('c', 'd', weight=25)

    def test_preserve_if_weight_greater_than_squelch(self):
        g = squelch(self.g, 10)
        self.assertEqual(3, len(g.edges()))

    def test_remove_if_less_than_squelch(self):
        g = squelch(self.g, 30)
        self.assertTrue(('c', 'd') not in g.edges())

    def test_remove_if_equal_to_squelch(self):
        g = squelch(self.g, 25)
        self.assertTrue(('c', 'd') not in g.edges())

if __name__ == "__main__":
    unittest.main()
