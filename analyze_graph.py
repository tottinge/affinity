import os
import sys
import re
import itertools
from datetime import datetime
from collections import defaultdict
import csv
import sqlite3
import networkx as nx

SQUELCH=10
MIN_GROUP_SIZE=5
DETAIL=False

DB_FILE=os.environ.get("EVENTS_DB_NAME", "events.sqlite.db")
print "DB:%s" % DB_FILE
if not os.path.exists(DB_FILE):
    print "DB file not found"
    exit(1)
database = sqlite3.connect(DB_FILE)

CSVFILE='edges.out'
if len(sys.argv) > 1:
    SQUELCH = int(sys.argv.pop(1))
print "Squelch:", SQUELCH
if len(sys.argv) >1:
    MIN_GROUP_SIZE=int(sys.argv.pop(1))
print "Min Size:", MIN_GROUP_SIZE
if len(sys.argv) >1:
    DETAIL=sys.argv.pop(1)


def node_weight(subgraph, node):
    node_weight = 0
    neighbors = subgraph.neighbors(node)
    for neighbor in neighbors:
        node_weight += subgraph[node][neighbor]["weight"]
    return node_weight, len(neighbors), name_for(node), node

def printable_edge(subgraph, edge):
    return subgraph.get_edge_data(*edge)["weight"], name_for(edge[0]), name_for(edge[1])

def name_for(file_id):
    if file_id in name_for.names:
        return name_for.names[file_id]
    cursor = database.cursor()
    cursor.execute(
        "SELECT source || ':' || path.pathname|| '/' || filename "
        " FROM path "
        " JOIN file ON path.id = file.path "
        " JOIN file_to_changeset f2c on f2c.file = file.id"
        " JOIN changeset on f2c.changeset = changeset.id "
        "WHERE file.id = ? ", 
        (file_id,)
    )
    results = cursor.fetchone()
    if results is None:
        return "unknown [%s]" % file_id
    name_for.names[file_id] = results[0]
    return results[0]
name_for.names = {}

def build_graph(squelch=SQUELCH):
    graph = nx.Graph()
    with open(CSVFILE) as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for (weight,left,right) in reader:
            weight = int(weight)
            if weight > squelch:
                lname = name_for(int(left))
                rname = name_for(int(right))
                if not ("_Test" in lname) and not ("_Test" in rname): 
                    graph.add_edge(left, right, weight=weight)
    return graph


def name_group(nodes):
    nameparts = defaultdict(lambda: 0)
    for node in nodes:
        for part in re.split('\W+', node[node.find(':')+1 : node.rfind('.')]):
            nameparts[part] += 1
    counted_names =((count,name) for (name,count) in nameparts.iteritems())
    ordered = sorted(counted_names, reverse=True)
    top = ".".join(name for (count,name) in ordered[:3])
    return top

def name_subgraph(subgraph):
    return name_group(name_for(x) for x in subgraph.nodes())

def build_affinity_groups(graph):
    subgraphs = list(
        x for x in nx.connected_component_subgraphs(graph) 
        if x.number_of_nodes()>=MIN_GROUP_SIZE
    )
    return subgraphs

