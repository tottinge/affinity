
import sys
import os
import sqlite3
from difflib import SequenceMatcher
from analyze_graph import *

def path_commonality(p1, p2):
    p1,_ = os.path.split(p1)
    p2,_ = os.path.split(p2)
    return "%d" % (SequenceMatcher(None, p1.split('/'), p2.split('/')).ratio() * 10)

def display_edges_and_path_commonality(subgraphs):
    buckets = {}
    for (number, subgraph) in enumerate(subgraphs):
        for edge in subgraph.edges():
            weight, left,right = printable_edge(subgraph, edge)
            print path_commonality(left, right), weight, left, right
        print ""

if __name__ == '__main__':
    G = build_graph()
    subgraphs = build_affinity_groups(G)
    display_edges_and_path_commonality(subgraphs)
