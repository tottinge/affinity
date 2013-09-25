from collections import namedtuple, defaultdict
from itertools import takewhile
import re

RecordResult = namedtuple("record", "description tickets files")

def gather_changesets(stream):
    while True:
        yield next_changeset(stream)

def next_changeset(stream):
    description = " ".join(x.strip() for x in takewhile(not_separator, stream))
    tickets = [ticket.upper() for ticket in tickets_from_description(description)]
    filenames = [f.strip() for f in takewhile(not_blank, stream)]
    if (not description) and (not filenames):
        raise StopIteration()
    return RecordResult(description, sorted(tickets), sorted(filenames))

def is_blank(line):
    return line.strip() == ''

def not_blank(line):
    return not is_blank(line)

divider = '-^-^*'
def not_separator(line):
    return line.strip() != divider

ticket_regex = re.compile('(?<!\w)(?:DE|QC|US)\d\d+', re.IGNORECASE)
def tickets_from_description(text):
    return set(ticket_regex.findall(text))

