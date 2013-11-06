from analyze_graph import *


def display_result_nodes(subgraphs):
    for subgraph in subgraphs:
        common_source = ""
        violations = set()

        name = name_subgraph(subgraph)
        print "%s: %d nodes %d edges" % (name, subgraph.number_of_nodes(), subgraph.number_of_edges())
        sorted_by_weight = sorted((node_weight(subgraph,node) for node in subgraph.nodes()), reverse=True)
        for (weight,popularity, filename, node) in sorted_by_weight:

            flag = "  "
            source = filename.split(":")[0]
            common_source = common_source or source
            if source != common_source:
                flag = ">>"
                violations.add(filename)

            print "\t", flag, weight, popularity, "%2.1f" % float(weight/float(popularity)), filename

            if DETAIL:
                neighborhood = [
                    (subgraph[node][neighbor]["weight"], name_for(neighbor))
                    for neighbor in subgraph.neighbors(node)
                ]
                neighborhood.sort(reverse=True)
                for (weight, neighbor) in neighborhood:
                    print "\t\t", weight, neighbor

        if violations:
            print "GROUP %s HAS %d CROSSOVER VIOLATIONS" % (name, len(violations))
            for filename in violations:
                print " ", filename

        print ""

if __name__ == '__main__':
    G = build_graph()
    subgraphs = build_affinity_groups(G)
    display_result_nodes(subgraphs)
