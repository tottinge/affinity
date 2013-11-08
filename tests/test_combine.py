import unittest
import networkx as nx
from conversion.combine_graphs import combine_graphs


class TestMe(unittest.TestCase):
    def setUp(self):
        self.g = nx.Graph()
        self.h = nx.Graph()

    def test_combine_empty_graphs(self):
        g, h = self.g, self.h
        gh = combine_graphs(g, h)
        self.assertEquals([], gh.nodes())

    def test_combine_preserves_original_node(self):
        g, h = self.g, self.h
        g.add_node('worked')
        gh = combine_graphs(g, h)
        assert 'worked' in gh.nodes()

    def test_combine_brings_nodes_in_from_right(self):
        g, h = self.g, self.h
        h.add_node('worked')
        gh = combine_graphs(g, h)
        assert 'worked' in gh.nodes()

    def test_preserves_edges_from_original(self):
        g, h = self.g, self.h
        g.add_edge('a', 'b')
        assert ('a', 'b') in combine_graphs(g, h).edges()

    def test_brings_edges_from_right(self):
        g, h = self.g, self.h
        h.add_edge('a', 'b')
        assert ('a', 'b') in combine_graphs(g, h).edges()

    def test_brings_edge_attributes_from_right(self):
        g, h = self.g, self.h
        h.add_edge('a', 'b', weight=4)
        gh = combine_graphs(g, h)
        self.assertEquals(4, gh.edge['a']['b']['weight'])

    def test_keeps_edge_attributes_from_left(self):
        g, h = self.g, self.h
        g.add_edge('a', 'b', weight=4)
        gh = combine_graphs(g, h)
        self.assertEquals(4, gh.edge['a']['b']['weight'])

    def test_weights_are_summed(self):
        g, h = self.g, self.h
        g.add_edge('a', 'b', weight=4)
        h.add_edge('a', 'b', weight=8)
        gh = combine_graphs(g, h)
        self.assertEquals(12, gh.edge['a']['b']['weight'])

    def test_reasons_are_appended(self):
        g, h = self.g, self.h
        g.add_edge('a', 'b', reason='ted')
        h.add_edge('a', 'b', reason='ignite')
        gh = combine_graphs(g, h)
        self.assertEquals(
            'ted,ignite',
            gh.get_edge_data('a', 'b')['reason']
        )


if __name__ == "__main__":
    unittest.main()
