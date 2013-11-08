#! python
# Parse records from HG logfiles (created using matchable.style)
# into records with descriptions, tickets, and files
# for use for further analysis

from collections import namedtuple
from itertools import takewhile
import re

ChangeSet = namedtuple(
    "changeset",
    "author date branch description tickets files"
)
ticket_regex = re.compile('(?<!\w)(?:DE|QC|US)\d\d+', re.IGNORECASE)
divider = '-^-^*'


def gather_changes(stream):
    while True:
        yield parse_changeset(stream)


def is_merge_or_backout(description):
    return any(
        map(
            lambda x: x in description,
            ['back out', 'backed out', 'backout', 'merge']
        )
    )


def not_separator(x):
    return (x.strip() != divider)


def not_blank(x):
    return bool(x.strip())


def tickets_from_description(text):
    return set(ticket_regex.findall(text))


def parse_changeset(stream):
    author = stream.next().decode('utf-8', 'replace').strip()
    date = stream.next().strip()
    branch = stream.next().strip()
    descr = " ".join(x.strip() for x in takewhile(not_separator, stream))
    tickets = set(
        list(tickets_from_description(descr))
        + list(tickets_from_description(branch))
    )
    files = ",".join(x.strip() for x in takewhile(not_blank, stream))
    return ChangeSet(author, date, branch, descr, tickets, files)
