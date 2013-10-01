#!/bin/bash
# takes about 6 minutes and generates 18,992,772 lines

OUT_DIR=${OUT_DIR:-.}
DB_NAME=${EVENTS_DB_NAME:-${OUT_DIR}/events.sqlite.db}

time sqlite3 $DB_NAME > ${OUT_DIR}/edges.out <<EOF
            select count(1) as weight
                    , l.file
                    , r.file
            from file_to_ticket l
                    , file_to_ticket r
            where l.ticket = r.ticket
                    and l.file < r.file
                    and l.ticket != ''
            group by l.file
                    , r.file
            having weight > 1
                and l.ticket not in
                        (select ticket from ticket_to_changeset where changeset = 5000)
            order by weight desc
;
EOF
