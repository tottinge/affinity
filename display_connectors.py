import sys
import os
import sqlite3
import itertools
from analyze_graph import *


def find_bridge_edges(raw, squelched):
    groups = build_affinity_groups(squelched)
    for (left,right) in itertools.combinations(groups, 2):

        left_node = left.nodes()[0]
        left_name = name_subgraph(left)
        
        right_node = right.nodes()[0]
        right_name = name_subgraph(right)

        bridge = set(nx.shortest_path(raw, left_node, right_node))
        chain = bridge .difference(left.nodes()) .difference(right.nodes())
        if chain:
            yield left_name, right_name, list(name_for(int(x)) for x in chain)

if __name__ == '__main__':
    if SQUELCH == 0:
        print>>sys.stdout, "No squelch, no analysis"
        sys.exit(1)

    squelched = build_graph()
    raw = build_graph(0)
    for (left,right,chain) in sorted(find_bridge_edges(raw, squelched)):
        print left, "---->", right
        print "\n   +--> ".join(chain)
        print 

