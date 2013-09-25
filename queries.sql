select count(*) from (
    select count(1) as weight
            , l.file
            , r.file
    from file_to_ticket l
            , file_to_ticket r
    where l.ticket = r.ticket
            and l.file != r.file
    group by l.file
            , r.file
);

