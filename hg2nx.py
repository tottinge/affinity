import sys
import fileinput
import networkx as nx
from hg_log_parser import gather_changes
import helpers


def graph_from_stream(repo_name, log_stream):
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
            helpers.reroute_and_delete(g, node_name)


def add_relationship(g, identifier, kind, files):
        g.add_node(identifier, kind=kind)
        g.add_edges_from(
            (identifier, filename)
            for filename in files
        )

if __name__ == "__main__":
    repo_name = sys.argv.pop(1)
    g = graph_from_stream(repo_name, fileinput.input())
    convert_reasons_to_edges(g)
    nx.write_graphml(g, sys.stdout, encoding='utf-8')
