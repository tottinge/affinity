select count(*), l.source, r.source
from cross_match
    join changeset l on l.id = cross_match.left_changeset                                                                                              
    join changeset r on r.id = cross_match.right_changeset
group by l.source, r.source;

