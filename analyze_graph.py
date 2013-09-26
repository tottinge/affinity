import os
import sys
import csv
import itertools
from datetime import datetime
import sqlite3
import networkx as nx


SQUELCH=10
if len(sys.argv) > 1:
    SQUELCH = int(sys.argv.pop(1))
print "Minimum weight considered =", SQUELCH

MIN_GROUP_SIZE=5
if len(sys.argv) >1:
    MIN_GROUP_SIZE=int(sys.argv.pop(1))
print "minimum group size =", MIN_GROUP_SIZE

DETAIL=False
if len(sys.argv) >1:
    DETAIL=sys.argv.pop(1)


DB_FILE="events.sqlite.db"
if not os.path.exists(DB_FILE):
    print "DB file not found"
    exit(1)
database = sqlite3.connect(DB_FILE)

CSVFILE='edges.out'


# get the dictionary name for a file id
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
        return "unknown [%d]" % file_id
    name_for.names[file_id] = results[0]
    return results[0]
name_for.names = {}

def build_graph():
    # Build the graph
    graph = nx.Graph()
    with open(CSVFILE) as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for (weight,left,right) in reader:
            weight = int(weight)
            if weight > SQUELCH:
                lname = name_for(int(left))
                rname = name_for(int(right))
                if not ("_Test" in lname) and not ("_Test" in rname): 
                    graph.add_edge(left, right, weight=weight)
    return graph


def build_affinity_groups(graph):
    # Analyze the graph, creating groups
    subgraphs = list(
        x for x in nx.connected_component_subgraphs(graph) 
        if x.number_of_nodes()>=MIN_GROUP_SIZE
    )
    print "# Subgraph: ", len(subgraphs)
    return subgraphs

# Produce results

def display_result_edges(subgraphs):
    for (number,subgraph) in enumerate(subgraphs):
        common_source = ""
        violations = set()

        print "group %d of len %d" % (number, subgraph.number_of_edges())
        #sorted_by_weight = sorted( (node_weight(subgraph,node) for node in subgraph.nodes()), reverse=True)
        #for (weight,popularity, filename, node) in sorted_by_weight:
        sorted_by_weight = sorted( (printable_edge(subgraph,edge) for edge in subgraph.edges()), reverse=True)
        for (weight,filename1, filename2) in sorted_by_weight:

    #        source = filename1.split(":")[0]
    #        common_source = common_source or source
    #        if source != common_source:
    #            print "<<<<<<< RED FLAG >>>>>>"
    #            violations.add(filename)

            #print "\t", weight, popularity, float(weight/float(popularity)), filename
            print "\t", weight, filename1, filename2

            if DETAIL:
                neighborhood = [ (subgraph[node][neighbor]["weight"], name_for(neighbor)) 
                                for neighbor in subgraph.neighbors(node) ]
                neighborhood.sort(reverse=True)
                for (weight, neighbor) in neighborhood:
                    print "\t\t", weight, neighbor

        if violations:
            print "GROUP %d HAS %d CROSSOVER VIOLATIONS" % (number, len(violations))
            for filename in violations:
                print "== ",filename

        print ""

def display_result_nodes(subgraphs):
    for (number,subgraph) in enumerate(subgraphs):
        common_source = ""
        violations = set()

        print "group %d of len %d" % (number, subgraph.number_of_edges())
        sorted_by_weight = sorted( (node_weight(subgraph,node) for node in subgraph.nodes()), reverse=True)
        for (weight,popularity, filename, node) in sorted_by_weight:

            flag = "  "
            source = filename.split(":")[0]
            common_source = common_source or source
            if source != common_source:
                flag = ">>"
                violations.add(filename)

            print "\t", flag, weight, popularity, "%2.1f" % float(weight/float(popularity)), filename

            if DETAIL:
                neighborhood = [ (subgraph[node][neighbor]["weight"], name_for(neighbor)) 
                                for neighbor in subgraph.neighbors(node) ]
                neighborhood.sort(reverse=True)
                for (weight, neighbor) in neighborhood:
                    print "\t\t", weight, neighbor

        if violations:
            print "GROUP %d HAS %d CROSSOVER VIOLATIONS" % (number, len(violations))
            for filename in violations:
                print " ",filename

        print ""

if __name__ == '__main__':
    G = build_graph()
    subgraphs = build_affinity_groups(G)
    #display_result_edges(subgraphs)
    display_result_nodes(subgraphs)
