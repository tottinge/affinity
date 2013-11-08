import unittest
import networkx as nx
from conversion.hg2nx import convert_reasons_to_edges


class TestNodeToEdgeConversion(unittest.TestCase):
    def setUp(self):
        g = self.g = nx.Graph()

        defect = 'DE1212'
        story = 'US1011'
        timestamp = '2013-10-29:tim'

        g.add_node(defect, kind='ticket')
        g.add_node(timestamp, kind='coincident')

        for node_name in 'a', 'b':
            g.add_edge(defect, node_name)
            g.add_edge(timestamp, node_name)

        g.add_node(story, kind='ticket')
        for node_name in 'a', 'c', 'd':
            g.add_edge(story, node_name)
            g.add_edge(timestamp, node_name)

        story2 = 'US2000'
        g.add_node(story2, kind='ticket')

        date2 = '1962-08-14:tim'
        g.add_node(date2, kind='coincident')
        for node_name in 'a', 'd', 'e':
            g.add_edge(story2, node_name)
            g.add_edge(date2, node_name)

    def test_file_nodes_remain_but_stories_and_coincidents_vanish(self):
        g = self.g
        convert_reasons_to_edges(g)
        self.assertEquals(set("abcde"), set(g.nodes()))

    def test_weight_and_reasons_are_coalesced(self):
        g = self.g
        convert_reasons_to_edges(g)
        ab_data = g.get_edge_data('a', 'b')
        self.assertEquals(2, ab_data['weight'])
        self.assertIn('DE1212', ab_data['reasons'])
        self.assertIn('2013-10-29:tim', ab_data['reasons'])
