from collections import namedtuple, defaultdict
from itertools import takewhile
import re

RecordResult = namedtuple("record", "description tickets files")

def isBlank(line):
    return line.strip() == ''

def notBlank(line):
    return not isBlank(line)


divider = '-^-^*'
def notSeparator(line):
    return line.strip() != divider


ticket_regex = re.compile('(?<!\w)(?:DE|QC|US)\d\d+', re.IGNORECASE)
def ticketsFromDescription(text):
    return set(ticket_regex.findall(text))


def gather_changesets(stream):
    while True:
        yield next_changeset(stream)

def next_changeset(stream):
    description = " ".join(x.strip() for x in takewhile(notSeparator, stream))
    tickets = [ticket.upper() for ticket in ticketsFromDescription(description)]
    filenames = [f.strip() for f in takewhile(notBlank, stream)]
    if (not description) and (not filenames):
        raise StopIteration()
    return RecordResult(description, sorted(tickets), sorted(filenames))

