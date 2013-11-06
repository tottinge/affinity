import networkx as nx
from helpers import reroute_and_delete
import unittest


class TestTicketNodes(unittest.TestCase):
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

    def test_me(self):
        g = self.g
        for node_name in g.nodes():
            node = g.node[node_name]
            if 'kind' in node:
                reroute_and_delete(g, node_name)
        self.assertEquals(set("abcde"), set(g.nodes()))
