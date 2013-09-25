SELECT a.id
        , a.source
	, b.id
	, b.source 
        , afiles.path
	, bfiles.path
FROM changeset a
   JOIN changeset b ON a.date = b.date AND a.user = b.user 
   JOIN files afiles ON a.id = afiles.changeset
   JOIN files bfiles ON b.id = bfiles.changeset
WHERE a.id != b.id
;
