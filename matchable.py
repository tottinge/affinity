"""
matchable.py

The purpose of this file is to filter a mercurial log (using matchable.style)
into a CSV we can use for other purposes.
"""
import sys
from collections import namedtuple
from itertools import takewhile
import fileinput
import csv
from hg_log_parser import divider, not_blank, not_separator, tickets_from_description

ChangeSet = namedtuple("changeset", "author date branch tickets files")

def gather_changes(stream):
    while True:
        yield parse_changeset(stream)

def parse_changeset(stream):
    author = stream.next().strip()
    date = stream.next().strip()
    branch=stream.next().strip()
    descr = " ".join(x.strip() for x in takewhile(not_separator, stream))
    tickets = set(list(tickets_from_description(descr)) + list(tickets_from_description(branch)))
    files = ",".join(x.strip() for x in takewhile(not_blank, stream))
    return ChangeSet(author, date, branch, tickets, files)

def main():
    repo = sys.argv.pop(1)
    writeme = csv.writer(sys.stdout) 
    for (ordinal,changeset) in enumerate(gather_changes(fileinput.input())):
        if not changeset.branch:
            continue
        if len(changeset.files) > 206:
            continue
        writeme.writerow([
            ordinal,
            repo,
            changeset.author,
            changeset.date, 
            changeset.branch,
            ",".join(changeset.tickets),
            changeset.files
        ])

if __name__ == "__main__":
    main()
