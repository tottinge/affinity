import sys
import os
import sqlite3
import itertools
from analyze_graph import *


def find_bridge_edges(raw, squelched):
    groups = build_affinity_groups(squelched)
    for (left,right) in itertools.combinations(groups, 2):

        left_name = name_subgraph(left)
        right_name = name_subgraph(right)

        boundary = nx.edge_boundary(raw, left.nodes(), right.nodes())
        if boundary:
            yield left_name, right_name, boundary


if __name__ == '__main__':
    if SQUELCH == 0:
        print>>sys.stdout, "No squelch, no analysis"
        sys.exit(1)

    squelched = build_graph()
    raw = build_graph(0)
    print ""
    for (left,right,chain) in sorted(find_bridge_edges(raw, squelched)):
        print left, "---->", right
        for (begin,end) in chain:
            print "   ",name_for(begin), name_for(end)
        print

