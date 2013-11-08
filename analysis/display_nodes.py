import sys
from analyze_graph import (
    parse_command_line,
    build_graph, name_subgraph,
    node_weight,
    build_affinity_groups,
    squelch
)


def show_heading(name, subgraph):
        print "%s: %d nodes %d edges" % (
            name,
            subgraph.number_of_nodes(),
            subgraph.number_of_edges()
        )


def display_result_nodes(subgraphs, verbose):
    for subgraph in subgraphs:
        common_source = ""
        violations = set()

        name = name_subgraph(subgraph)
        show_heading(name, subgraph)

        sorted_by_weight = sorted(
            (node_weight(subgraph, node) for node in subgraph.nodes()),
            reverse=True
        )

        for (weight, popularity, filename, node) in sorted_by_weight:
            flag = "  "
            source = filename.split(":")[0]
            common_source = common_source or source
            if source != common_source:
                flag = ">>"
                violations.add(filename)

            print "\t%s %s %s %2.1f %s" % (
                flag,
                weight,
                popularity,
                float(weight / float(popularity)),
                filename
            )

            if verbose:
                display_detail(subgraph, node)

        if violations:
            display_violations(name, violations)

        print ""


def display_violations(name, violations):
    print "GROUP %s HAS %d CROSSOVER VIOLATIONS" % (
        name,
        len(violations)
    )
    for filename in violations:
        print " ", filename


def display_detail(subgraph, node):
    neighborhood = [
        (subgraph[node][neighbor]["weight"], neighbor)
        for neighbor in subgraph.neighbors(node)
    ]
    neighborhood.sort(reverse=True)
    for (weight, neighbor) in neighborhood:
        print "\t\t", weight, neighbor


if __name__ == '__main__':
    args = parse_command_line(*sys.argv[1:])
    G = build_graph(args.inputfile)
    G = squelch(G, args.squelch)
    subgraphs = build_affinity_groups(G, args.minsize)
    display_result_nodes(subgraphs, args.verbose)
