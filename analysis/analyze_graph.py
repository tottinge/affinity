import re
from collections import defaultdict
import networkx as nx
import argparse


def parse_command_line(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'squelch',
        type=int,
        help='eliminate lower-weighted edges'
    )
    parser.add_argument(
        'minsize',
        type=int,
        help='ignore smaller groups'
    )
    parser.add_argument(
        'inputfile',
        type=argparse.FileType('r'),
        help="graphml file"
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='show details'
    )
    args = parser.parse_args(list(args))
    return args


def build_graph(stream):
    return nx.read_graphml(stream)


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


def squelch(graph, squelch):
    squelched = graph.copy()
    squelched.remove_edges_from(
        edge
        for edge in graph.edges_iter()
        if graph.get_edge_data(*edge)['weight'] <= squelch
    )
    return squelched


def build_affinity_groups(graph, groupsize):
    subgraphs = list(
        x for x in nx.connected_component_subgraphs(graph)
        if x.number_of_nodes() >= groupsize
    )
    return subgraphs
