from heatmap import gather_changesets
from collections import defaultdict
from itertools import combinations
import fileinput
import shelve
import tempfile
import squeezepath
import os

squeezer = squeezepath.SqueezePath()

def get_weighted_edges(stream, all_edges):
    for record in gather_changesets(stream):
        for edge in combinations(record.files, 2):
            edge = map(squeezer.encode, edge)
            string_edge = "|".join(sorted(edge))

            oldsum = all_edges.get(string_edge, 0)
            all_edges[string_edge] = (oldsum + 1)
    return all_edges

def toss_least_significant(edges):
    if not edges:
        return edges
    mean = sum(edges.itervalues())/len(edges)
    half_mean = mean*.5
    return dict( 
        (key,value) for (key,value) in edges.iteritems()
        if value > 1 and value > half_mean
    );

def print_edges(edges):
    for edge,weight in sorted(edges.iteritems(), reverse=True):
        nodes = edge.split("|")
        nodes = map(squeezer.decode, nodes)
        print weight, nodes

def main():
    dbfilename = tempfile.mktemp(prefix='shelve')
    store = shelve.open(dbfilename)
    try:
        weighted = get_weighted_edges(
            fileinput.input(), 
            store
        )
        significant = toss_least_significant(weighted)
        print_edges(significant)
    finally:
        store.close()
        os.unlink(dbfilename)

if __name__ == "__main__":
    main()


