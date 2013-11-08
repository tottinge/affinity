import sys
from analyze_graph import (
    parse_command_line,
    build_graph,
    build_affinity_groups,
    printable_edge
)


def display_fs_spanning_edges(subgraphs):
    problem_neighbors = set()
    for (number, subgraph) in enumerate(subgraphs):
        for edge in subgraph.edges():
            (weight, f1, f2) = printable_edge(subgraph, edge)
            src, fname = f1.split(':')
            if not f2.startswith(src):
                print weight, f1, f2
                edge_tuple = tuple(sorted([f1, f2]) + [weight])
                problem_neighbors.add(edge_tuple)
    print ""
    for (left, right, weight) in sorted(problem_neighbors):
        print weight, left, right


if __name__ == '__main__':
    args = parse_command_line(*sys.argv[1:])
    G = build_graph(args.inputfile)
    subgraphs = build_affinity_groups(G, args.squelch)
    display_fs_spanning_edges(subgraphs)
