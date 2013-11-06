# Helpers
from itertools import combinations


def reroute_and_delete(g, node_name):
    _annotate_and_route_around(g, node_name)
    _detach_and_delete(g, node_name)


def _annotate_and_route_around(g, node_name):
    # Also could already exist, but I didn't find it in networkx
    # Just as well, because 'weight' and 'reasons' are helpful to me
    for (left, right) in combinations(g.neighbors(node_name), 2):
        if g.has_edge(left, right):
            g[left][right]['weight'] += 1
            g[left][right]['reasons'] += ("," + node_name)
        else:
            g.add_edge(left, right, weight=1)
            g[left][right]['reasons'] = node_name


def _detach_and_delete(g, node_name):
    # I suspect this is already in existence under a different name
    # Need a little research
    for neighbor_name in g.neighbors(node_name):
        g.remove_edge(node_name, neighbor_name)
    g.remove_node(node_name)
