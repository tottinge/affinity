import sys
import os
from difflib import SequenceMatcher
from analyze_graph import (
    parse_command_line,
    build_graph,
    build_affinity_groups,
    printable_edge
)


def path_commonality(p1, p2):
    p1, _ = os.path.split(p1)
    p2, _ = os.path.split(p2)
    commonality = SequenceMatcher(
        None,
        p1.split('/'),
        p2.split('/')
    ).ratio() * 10
    return "%d" % (commonality,)


def display_edges_and_path_commonality(subgraphs):
    for (number, subgraph) in enumerate(subgraphs):
        for edge in subgraph.edges():
            weight, left, right = printable_edge(subgraph, edge)
            print path_commonality(left, right), weight, left, right
        print ""


if __name__ == '__main__':
    args = parse_command_line(*sys.argv[1:])
    G = build_graph(args.inputfile)
    subgraphs = build_affinity_groups(G, args.squelch)
    display_edges_and_path_commonality(subgraphs)
