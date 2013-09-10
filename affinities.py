from hg_log_parser import gather_changesets
from collections import defaultdict
from itertools import combinations
import fileinput
import shelve
import tempfile
import squeezepath
import os


squeezer = squeezepath.SqueezePath()
class Edge(object):
    def __init__(self, *nodes):
        left,right = nodes
        left = squeezer.encode(left)
        right = squeezer.encode(right)
        self.short = "|".join([left,right])
    def _getleft(self):
        left = self.short.split("|")[0]
        return squeezer.decode(left)
    def _getright(self):
        right = self.short.split("|")[1]
        return squeezer.decode(right)
    left = property(_getleft,None, None,"Left node of edge")
    right =property(_getright,None, None, "Right node of edge")
    def __repr__(self):
        return "Edge: {%s, %s}" % (self.left, self.right)
    def __cmp__(self, other):
        return cmp(self.short,other.short)
    def __hash__(self):
        return hash(self.short)

def interesting_files(filelist):
    for filename in filelist:
        ignore = '.png','.pyc','.ts','.htm','.hhc','.ini'
        if any( map(filename.endswith, ignore)):
            continue
        yield filename

def interesting_changesets(stream):
    for changeset in stream:
        description = changeset.description.lower()
        if 'merge' in description:
            continue
        if 'backed out' in description:
            continue
        if 'back out' in description:
            continue
        yield changeset


def get_weighted_edges(stream, all_edges=None):
    all_edges = all_edges or {}
    for record in interesting_changesets(gather_changesets(stream)):
        filegroup = interesting_files(record.files)
        for edge in combinations(filegroup, 2):
            myedge = Edge(*edge)
            oldsum = all_edges.get(myedge, 0)
            all_edges[myedge] = (oldsum + 1)
    return all_edges

def toss_least_significant(edges):
    if edges:
        mean = sum(edges.itervalues())/len(edges)
        half_mean = mean*.5
        limit = max(2,half_mean)
        for key in edges.keys():
            if edges[key] < limit:
                del edges[key]
    return edges

def print_edges(edges):
    for edge,weight in sorted(edges.iteritems(), reverse=True):
        print weight, edge.left, edge.right

def main():
    dbfilename = tempfile.mktemp(prefix='shelve')
    store = shelve.open(dbfilename, writeback=True)
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


