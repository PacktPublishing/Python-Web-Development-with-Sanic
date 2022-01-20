SELECT s.series_id,
    s.name,
    e.eid
FROM series s
    JOIN eids e ON s.ref_id = e.ref_id
WHERE e.eid = :eid;
