SELECT e.eid,
    s.series_id,
    s.name
FROM series s
    JOIN eids e ON s.ref_id = e.ref_id
LIMIT :limit OFFSET :offset;
