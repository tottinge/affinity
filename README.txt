Main part of analysis program
   ./runme.sh -- main script to make stuff happen
   ./repositories.config -- a list of HG repos to search
   ./matchable.style - format specification for hg logs
   ./hg_log_parser.py - Parse mercurial logs (created with matchable style)
   ./display*py - various analyses of the data
   ./helpers.py - some utilities

Analyses:
    display_edges.py - Show edges in affinity groups
    display_nodes.py - Show nodes in affinity groups
    display_spanning_edges.py - show FS-spanning relationships
    display_path_correlation.py - show edges along with path commonality


