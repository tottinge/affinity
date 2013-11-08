import sys
import itertools
import networkx as nx
from analyze_graph import (
    build_graph,
    build_affinity_groups,
    parse_command_line,
    squelch,
    name_subgraph
)


def find_bridge_edges(raw, squelched, groupsize):
    groups = build_affinity_groups(squelched, groupsize)
    for (left, right) in itertools.combinations(groups, 2):
        left_name = name_subgraph(left)
        right_name = name_subgraph(right)
        boundary = nx.edge_boundary(raw, left.nodes(), right.nodes())
        if boundary:
            yield left_name, right_name, boundary


if __name__ == '__main__':
    args = parse_command_line(*sys.argv[1:])
    if args.squelch == 0:
        print>>sys.stdout, "No squelch, no analysis"
        sys.exit(1)

    raw = build_graph(args.inputfile)
    squelched = squelch(raw, args.squelch)
    bridge_edges = find_bridge_edges(raw, squelched, args.minsize)

    print ""
    for (left, right, chain) in sorted(bridge_edges):
        print left, "---->", right
        for (begin, end) in chain:
            print "   ", begin, end
        print
