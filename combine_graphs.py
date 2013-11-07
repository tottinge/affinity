import os
import sys
import networkx as nx


def edge_data_for(graph, x, y):
    return graph.get_edge_data(x, y) or {}


def combine_graphs(left, right):
    new_graph = left.copy()
    new_graph.add_nodes_from(right)
    for (first, second) in right.edges_iter():
        both = [
            edge_data_for(left, first, second),
            edge_data_for(right, first, second),
        ]
        newdata = {
            'weight': sum(x.get('weight', 0) for x in both),
            'reason': ",".join(x.get('reason', '') for x in both),
        }
        new_graph.add_edge(first, second, **newdata)
    return new_graph


def graph_from_file(filename):
    try:
        return nx.read_graphml(filename)
    except Exception as fred:
        print>>sys.stderr, fred
        print "FAILED: SKIPPED"
    return nx.Graph()


def combine_all(filenames):
    graphs = (
        graph_from_file(filename)
        for filename in filenames
        if os.path.exists(filename) and os.path.getsize(filename) > 0
    )
    return reduce(combine_graphs, graphs, nx.Graph())

if __name__ == "__main__":
    graph = combine_all(sys.argv[1:])
    nx.write_graphml(graph, sys.stdout, encoding='utf-8')
