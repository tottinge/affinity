CREATE TABLE cross_match AS
SELECT afiles.id as left, 
       bfiles.id as right, 
       a.id as left_changeset, 
       b.id as right_changeset
FROM changeset a
   JOIN changeset b ON a.date = b.date AND a.user = b.user 
   JOIN files afiles ON a.id = afiles.changeset
   JOIN files bfiles ON b.id = bfiles.changeset
WHERE a.id != b.id
AND a.source != b.source
;
