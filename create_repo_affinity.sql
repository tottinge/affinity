create table file_match as 
select l.source as lsource, lf.path as leftpath, r.source as rsource, rf.path as rpath
from cross_match
    join changeset l on l.id = cross_match.left_changeset                                                                                              
        join files lf on lf.changeset = l.id
    join changeset r on r.id = cross_match.right_changeset
        join files rf on rf.changeset = r.id 
where l.source != r.source;

-- select count(*) as times, lsource, rsource, rpath FROM file_match GROUP BY lsource, rsource, rpath ORDER BY times;
