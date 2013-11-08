import sys
import fileinput
import networkx as nx
from itertools import combinations

# The following is the only mercurial-related bit in this file
# it is otherwise not remotely hg-related.
# Maybe there should be a flag?
import hg_log_parser


def graph_from_stream(repo_name, log_stream, gather_changes):
    g = nx.Graph()
    for record in gather_changes(log_stream):
        files = [
            repo_name + ':' + filename
            for filename in record.files.split(',')
        ]

        identifier = "%s:%s" % (record.author, record.date)
        add_relationship(g, identifier, 'coincident', files)

        # Add tickets
        for ticket in record.tickets:
            add_relationship(g, ticket, 'ticket', files)
    return g


def convert_reasons_to_edges(g):
    for node_name in g.nodes():
        kind = g.node[node_name].get('kind', None)
        if kind in ['coincident', 'ticket']:
            reroute_and_delete(g, node_name)


def add_relationship(g, identifier, kind, files):
        g.add_node(identifier, kind=kind)
        g.add_edges_from(
            (identifier, filename)
            for filename in files
        )


def reroute_and_delete(g, node_name):
    _annotate_and_route_around(g, node_name)
    _detach_and_delete(g, node_name)


def _annotate_and_route_around(g, node_name):
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


if __name__ == "__main__":
    repo_name = sys.argv.pop(1)
    g = graph_from_stream(
        repo_name,
        fileinput.input(),
        hg_log_parser.gather_changes
    )
    convert_reasons_to_edges(g)
    nx.write_graphml(g, sys.stdout, encoding='utf-8')
