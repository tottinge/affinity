# Calculate heat map from hg logs
import sys
import re
from itertools import takewhile
from collections import namedtuple, defaultdict
import fileinput
import getopt

divider = '-^-^*'

ArgsType = namedtuple("Args","files filters")
RecordResult = namedtuple("record", "tickets files")

def isBlank(line):
    return line.strip() == ''

def notSeparator(line):
    return line.strip() != divider

def notBlank(line):
    return not isBlank(line)


def gather_changesets(stream):
    while True:
        yield next_changeset(stream)

def next_changeset(stream):
    description = " ".join(x.strip() for x in takewhile(notSeparator, stream))
    tickets = [ticket.upper() for ticket in ticketsFromDescription(description)]
    filenames = [f.strip() for f in takewhile(notBlank, stream)]
    if (not description) and (not filenames):
        raise StopIteration()
    return RecordResult(sorted(tickets),sorted(filenames))

ticket_regex = re.compile('(?<!\w)(?:DE|QC|US)\d\d+', re.IGNORECASE)
def ticketsFromDescription(text):
    return set(ticket_regex.findall(text))

def collect(stream):
    tickets_per_file = defaultdict(set)
    for changeset in gather_changesets(stream):
        for filename in changeset.files:
            tickets_per_file[filename].update(changeset.tickets)
    return tickets_per_file

def handle_arguments(arguments):
    opts, files = getopt.getopt(arguments, "f:")
    opts = dict(opts)
    return ArgsType(files=files, filters=opts.get('-f',None))

def filter_by_keyword(dataset, patterns):
    return ( (key,value)
             for key,value in dataset.iteritems()
             for pattern in patterns 
             if pattern in key)

def calculate_heat(source, tickets):
    stories = len([ticket for ticket in tickets if ticket.startswith("US")])
    defects = len(tickets) - stories
    return len(tickets), defects

def prepareForDisplay(data):
    for filename, tickets in data:
        stories,defects = calculate_heat(filename, tickets)
        if stories:
            yield (stories, defects, filename, sorted(tickets))

def print_heatdata(source, filters):
    raw_data = collect(source)
    if filters:
        tickets_by_filename = filter_by_keyword(raw_data,filters)
    else:
        tickets_by_filename = raw_data.iteritems()

    for record in sorted(prepareForDisplay(tickets_by_filename), reverse=True):
        stories,defects,filename,tickets = record
        tickets= ",".join(tickets)
        print "%d,%d,%s" % (stories, defects, filename)

if __name__ == "__main__":
    arguments = handle_arguments(sys.argv[1:])
    if arguments.files:
        source = fileinput.input(arguments.files)
    else:
        source = sys.stdin
    filters = None
    if arguments.filters:
        filters = [ f.strip() for f in open(arguments.filters).readlines()]
    print_heatdata(source,filters)

