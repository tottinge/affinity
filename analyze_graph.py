import sys
import re
from collections import defaultdict
import networkx as nx

SQUELCH = 10
MIN_GROUP_SIZE = 5
DETAIL = False

if len(sys.argv) > 1:
    SQUELCH = int(sys.argv.pop(1))
print "Squelch:", SQUELCH
if len(sys.argv) > 1:
    MIN_GROUP_SIZE = int(sys.argv.pop(1))
print "Min Size:", MIN_GROUP_SIZE
if len(sys.argv) > 1:
    DETAIL = sys.argv.pop(1)


def build_graph(stream = None):
    if not stream:
        import fileinput
        stream = fileinput.input()
    return nx.read_graphml(stream, encoding='utf-8')


def node_weight(subgraph, node):
    neighbors = subgraph.neighbors(node)
    node_weight = sum(
        subgraph[node][neighbor]["weight"]
        for neighbor in neighbors
    )
    return node_weight, len(neighbors), node, node


def printable_edge(subgraph, edge):
    return subgraph.get_edge_data(*edge)["weight"], edge[0], edge[1]


def name_group(nodes):
    nameparts = defaultdict(lambda: 0)
    for node in nodes:
        for part in re.split('\W+', node[node.find(':') + 1: node.rfind('.')]):
            nameparts[part] += 1
    counted_names = ((count, name) for (name, count) in nameparts.iteritems())
    ordered = sorted(counted_names, reverse=True)
    top = ".".join(name for (count, name) in ordered[:3])
    return top


def name_subgraph(subgraph):
    return name_group(subgraph.nodes())


def build_affinity_groups(graph):
    subgraphs = list(
        x for x in nx.connected_component_subgraphs(graph)
        if x.number_of_nodes() >= MIN_GROUP_SIZE
    )
    return subgraphs
