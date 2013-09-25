#!/bin/bash
# takes about 6 minutes and generates 18,992,772 lines
time sqlite3 events.sqlite.db > edges.out <<EOF
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

#time sqlite3 events.sqlite.db > tickets.out <<EOF
#        select t.handle as ticket, count(1) as num_files
#        from file_to_ticket as ft, ticket as t
#        where ft.ticket = t.id
#        group by t.handle
#        order by num_files desc
#;
#EOF


