import networkx as nx
import csv
import itertools
from datetime import datetime
import sqlite3

database = sqlite3.connect("events.sqlite.db")

names = dict()
def name_for(file_id):
    if file_id in names:
        return names[file_id]
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
        return "unknown [%d]" % file_id
    names[file_id] = results[0]
    return results[0]



squelch=0
G = nx.Graph()
with open('edges.out') as csvfile:
    reader = csv.reader(csvfile, delimiter="|")
    for (weight,left,right) in reader:
        weight = int(weight)
        if weight > squelch:
            lname = name_for(int(left))
            rname = name_for(int(right))
            if not ("_Test" in lname) and not ("_Test" in rname): 
                G.add_edge(left, right, weight=weight)

subgraphs = list(nx.connected_components(G))

print "# Subgraphs: ", len(subgraphs)
for subgraph in subgraphs:
    print "Len: ", len(subgraph)
    for f in sorted(map(name_for, subgraph)):
        print "\t", f
