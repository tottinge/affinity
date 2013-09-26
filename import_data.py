import os
import sys
import csv
import fileinput
import sqlite3

def get_database(filename):
    schema = """
    create table changeset (
        id INTEGER PRIMARY KEY,
        ordinal INTEGER, 
        source TEXT, 
        date TEXT, 
        user TEXT
    );
    create table ticket (
        id INTEGER PRIMARY KEY,
        changeset INTEGER,
        handle TEXT,
        FOREIGN KEY (changeset) REFERENCES changeset(id)
    );
    create table ticket_to_changeset (
        changeset INTEGER,
        ticket INTEGER,
        FOREIGN KEY (changeset) REFERENCES changeset(id),
        FOREIGN KEY (ticket) references ticket(id)
    );
    create table file (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        path INTEGER,
        FOREIGN KEY (path) references path(id)

    );
    create table file_to_changeset (
        file INTEGER,
        changeset INTEGER,
        FOREIGN KEY (changeset) REFERENCES changeset(id),
        FOREIGN KEY (file) references file(id)
    );
    create table path (
        id INTEGER PRIMARY KEY,
        pathname TEXT
    );
    create table file_to_ticket (
        file INTEGER,
        ticket INTEGER,
        FOREIGN KEY (file) references file(id),
        FOREIGN KEY (ticket) references ticket(id)
    );
    create table area (
        id INTEGER PRIMARY KEY,
        dir TEXT,
        changeset INTEGER,
        FOREIGN KEY (changeset) REFERENCES changeset(id)
    );
    """
    if os.path.exists(filename):
        os.unlink(filename)
    database = sqlite3.connect(filename)
    database.text_factory = str
    database.executescript(schema)
    return database

def prefilter(stream):
    csv_hard_limit = 131072
    for item in stream:
        if len(item) < csv_hard_limit :
            yield item
        else:
            print>>sys.stderr, "Too much for csv:", item

def record_import(inputstream, database):
    reader = csv.reader(prefilter(fileinput.input()))
    for index, row in enumerate(reader):

        # populate changeset
        cursor = database.cursor()
        ordinal, source, user, date, branch, tickets, files = row
        split_files = files.split(',')
        if len(split_files) > 206:
            continue
        if 'auryn' in branch.lower():
            continue

        cursor.execute(
            "INSERT INTO changeset (ordinal, source, date, user)"
            " VALUES (?,?,?,?)", 
            (ordinal, source, date, user)
        )
        changeset_id = cursor.lastrowid

        ticket_names = tickets.split(',')
        ticket_names.append(user + ' ' + date)
        ticket_ids = ticket_ids_for(ticket_names, database)
        for ticket_id in ticket_ids:
            cursor.execute(
                "INSERT INTO ticket_to_changeset (ticket, changeset)"
                " VALUES (?,?)",
                (ticket_id, changeset_id)
            )
        
        # Populate information about the files
        for filepath in split_files:
            filepath = filepath.strip()
            if not filepath:
                continue

            # File and directory
            directory, filename = os.path.split(filepath)
            important_endings = ['.h','.cpp','.txt','.xml','.ui']
            if not any(map(filename.endswith, important_endings)):
                continue

            directory_id = path_key_for(directory, database)
            file_id = file_id_for(filename, directory_id, database)

            associate_files_to_tickets(file_id, ticket_ids, database)
                

            # File to Changeset
            cursor.execute(
                "INSERT INTO file_to_changeset (changeset, file) VALUES (?,?)",
                (changeset_id, file_id)
            )

            # (Denormalization) area
#            cursor.execute(
#                "INSERT INTO area (changeset, dir)"
#                " VALUES (?,?)", 
#                (changeset_id, area_from(filepath))
#            )

            # commit often for performance reasons
            if index % 200 == 0:
                database.commit

        # Leave database in consistent state
        database.commit()


def area_from(filepath):
    paths = filepath.strip().split("/")
    path = ''
    if len(paths) > 1:
        # GSX unfortunately has an extra directory level 
        if paths[0] == 'GSX':
            path = paths[0] + '/' + paths[1]
        else:
            path = paths[0]
    return path


class memoized(object):
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = []

    def __call__(self, function):
        def wrapped(*given_args):
            cached = [ value for (args,value) in self.cache if args == given_args]
            if cached:
                result = cached[0]
            else:
                result = function(*given_args)
                cache_item = (given_args, result)
                self.cache.append(cache_item)
                if len(self.cache)>self.cache_size:
                    self.cache.pop(0)
            return result
        return wrapped

    def __str__(self):
        return str(cache)

@memoized(cache_size=10)
def path_key_for(path, db):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM path WHERE pathname=?", [path])
    key = cursor.fetchone()
    if key is None:
        cursor.execute("INSERT INTO path (pathname) VALUES (?)", [path])
        key = cursor.lastrowid
    else:
        (key,) = key
    return key

@memoized(cache_size=2000)
def file_id_for(filename, directory_id, database):
    cursor = database.cursor()
    cursor.execute("SELECT id FROM file WHERE filename=? and path = ?", [filename, directory_id])
    key = cursor.fetchone()
    if key is None:
        cursor.execute(
            "INSERT INTO file (path, filename)"
            " VALUES (?,?)", 
            (directory_id, filename)
        )
        return cursor.lastrowid
    else:
        return key[0]

@memoized(cache_size=20)
def ticket_id_for(database, ticket):
        cursor = database.cursor()
        handle = ticket.strip()
        cursor.execute("SELECT id FROM ticket WHERE handle=?", [handle])
        key = cursor.fetchone()
        if key is None:
            cursor.execute(
                "INSERT INTO ticket (handle)"
                " VALUES (?)", 
                (handle,)
            )
            return cursor.lastrowid
        else:
            return key[0]


def ticket_ids_for(tickets, database):
        cursor = database.cursor()
        return [ticket_id_for(database, ticket) for ticket in tickets]

@memoized(cache_size=40)
def insert_file_to_ticket(file_id, ticket_id, database):
    cursor = database.cursor()
    cursor.execute(
        "SELECT * FROM file_to_ticket "
        "where file=? and ticket=?",
        (file_id, ticket_id))
    key = cursor.fetchone()
    if key is None:
        cursor.execute(
            "INSERT INTO file_to_ticket (file, ticket)"
            " VALUES (?, ?)",
            (file_id, ticket_id))


def associate_files_to_tickets(file_id, ticket_ids, database):
    for ticket_id in ticket_ids:
        insert_file_to_ticket(file_id, ticket_id, database)

if __name__ == "__main__":
    database = get_database("events.sqlite.db")
    record_import(fileinput.input(), database)
    database.close()

