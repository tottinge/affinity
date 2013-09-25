-- select * from data as d1, data as d2 where d1.date = d2.date and d1.user = d2.user and d1.files not in ('', 'build.env') and d2.files not in ('', 'build.env') and (d1.row != d2.row or d1.source != d2.source) and d1.files != d2.files limit 10;
-- select * from tickets as t, changeset as c where t.changeset = c.id and t.handle != '';
-- select t.handle, c.source, c.date, c.user from tickets as t, changeset as c where t.changeset = c.id and t.handle != '' order by t.handle;
-- select t.handle, c.source, c.date, c.user, f.path from tickets as t, changeset as c, files as f where t.changeset = c.id and f.changeset = c.id and t.handle != '' and f.path != '' order by t.handle ;
-- select sum(1), t.handle, c.source, c.date, c.user, f.path from tickets as t, changeset as c, files as f where t.changeset = c.id and f.changeset = c.id and t.handle != '' and f.path != '' group by t.handle, f.path;
-- select t.handle, c.source, c.date, c.user from tickets as t, changeset as c where t.changeset = c.id and t.handle != '';

-- create table events (id INTEGER PRIMARY KEY AUTOINCREMENT, name);
-- -- -- --  finding events by source, date, etc (team?, what else?)
select distinct t.handle, c.source, c.date, c.user from tickets as t, changeset as c where t.changeset = c.id and t.handle != '' order by t.handle;
-- -- -- --  finding events by handle:
-- insert into events (name) select distinct t.handle from tickets as t, changeset as c where t.changeset = c.id and t.handle != '';
-- alter table changeset add column event integer;
select * from events e, changeset c1, changeset c2, files f1, files f2 where e.id = c1.event_id and e.id = c2.event_id and f1.changeset = c1.id and f2.changeset = c2.id and c1.path != c2.path

update changeset set event = (select e.id from events as e, tickets as t where t.changeset = changeset.id and e.name = t.handle);


-- get number of changesets per ticket
select count(1) as numChanges, c.source, t.handle as handle from changeset c, tickets t, events e where c.id = t.changeset and t.handle = e.name group by t.handle, c.source limit 10;


---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------
-- The following queries assume that we're using ticket names to tie together commits between repos.
-- We'd like to find another way to tie together commits between repos.
---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

-- get number of tickets per source
select count(1) as numInSource, source from (select count(1) as numChanges, c.source as source, t.handle as handle from changeset c, tickets t, events e where c.id = t.changeset and t.handle = e.name group by t.handle, c.source) group by source limit 10;
-- get number of tickets per source-pair
select count(1) as numTickets, srcs from (select group_concat(src) as srcs, handle from (select c.source as src, t.handle as handle from changeset c, tickets t, events e where c.id = t.changeset and t.handle = e.name and c.date => '2013-05-01' group by t.handle, c.source) group by handle) group by srcs limit 30;

-- WORKING
-- get number of (non-pinning) tickets per source-pair per directory
-- Count ticket for each source pair
select count(1) as numTickets, dir, group_concat(src) from (
    select c.source || "/" || a.dir as dir,
        -- c.id as changeset_id,
        c.source as src,
        t.handle as ticket
    from areas a, changeset c, tickets t where
        a.dir not like '%build.env%' and
        a.changeset = c.id and c.date >= '2013-04-99' and
        t.changeset = c.id
        and t.handle != ''
    group by dir, src, ticket
        -- ,changeset_id
    ) group by dir, ticket
    order by numTickets asc;

-- get number of (non-pinning) tickets per source-pair 
-- Count ticket for each source pair
select count(1) as numTickets, srcs from (
        -- Coelesce sources for each ticket
        select group_concat(src) as srcs, handle from (
                -- All ticket/source pairs
                select changeset_id, src, t.handle as handle from (
                        -- All changesets which dont include only build.env and after the repo split
                        select c.id as changeset_id, c.source as src from files f, changeset c where
                                -- f.path != 'build.env' and
                                f.changeset = c.id and c.date >= '2013-04-99'
                ), tickets t, events e where changeset_id = t.changeset and t.handle = e.name group by t.handle, src
         ) group by handle)
group by srcs limit 30;



-- number of changesets per source
select count(1) as cnt, c.source as src from changeset c, events e, tickets t where t.changeset = c.id and e.name = t.handle group by c.source;
-- number of changesets per source-pair
select sum(numEvents) as totEvents, srcs from (select count(1) as cnt1, group_concat(src) as srcs, sum(cnt) as numEvents, handle from (select count(1) as cnt, c.source as src, t.handle as handle from changeset c, events e, tickets t where t.changeset = c.id and e.name = t.handle group by c.source, t.handle order by t.handle) group by handle) group by srcs;
