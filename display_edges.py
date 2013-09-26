import sys
import os
import sqlite3
from analyze_graph import *

def display_result_edges(subgraphs):
    for (number,subgraph) in enumerate(subgraphs):
        print "group %d of len %d" % (number, subgraph.number_of_edges())
        sorted_by_weight = sorted( (printable_edge(subgraph,edge) for edge in subgraph.edges()), reverse=True)
        for (weight,filename1, filename2) in sorted_by_weight:
            print "\t", weight, filename1, filename2
        print ""

if __name__ == '__main__':
    G = build_graph()
    subgraphs = build_affinity_groups(G)
    display_result_edges(subgraphs)
