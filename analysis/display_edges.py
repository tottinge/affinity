import sys
from analyze_graph import (
    build_graph,
    build_affinity_groups,
    parse_command_line,
    printable_edge
)


def display_result_edges(subgraphs):
    for (number, subgraph) in enumerate(subgraphs):
        print "group %d of len %d" % (number, subgraph.number_of_edges())
        sorted_by_weight = sorted(
            (printable_edge(subgraph, edge) for edge in subgraph.edges()),
            reverse=True
        )
        for (weight, filename1, filename2) in sorted_by_weight:
            print "\t", weight, filename1, filename2
        print ""

if __name__ == '__main__':
    args = parse_command_line(*sys.argv[1:])
    G = build_graph(args.inputfile)
    subgraphs = build_affinity_groups(G, args.squelch)
    display_result_edges(subgraphs)
