
import sys
import os
import sqlite3
from analyze_graph import *

def display_fs_spanning_edges(subgraphs):
    problem_neighbors = set()
    for (number,subgraph) in enumerate(subgraphs):
        for edge in subgraph.edges():
            (weight, f1, f2)  = printable_edge(subgraph, edge)
            src,fname = f1.split(':')
            if not f2.startswith(src):
                print weight, f1, f2
                edge_tuple = tuple(sorted([f1,f2])+[weight])
                problem_neighbors.add(edge_tuple)
    print ""
    for (left,right,weight) in sorted(problem_neighbors):
        print weight, left, right
    

if __name__ == '__main__':
    G = build_graph()
    subgraphs = build_affinity_groups(G)
    display_fs_spanning_edges(subgraphs)
