SELECT e.eid,
    b.book_id,
    b.title,
    COALESCE(
        (
            SELECT json_build_object('name', a.name, 'eid', ae.eid)
            FROM authors a
                JOIN eids ae ON a.ref_id = ae.ref_id
            WHERE a.author_id = b.author_id
        ),
        '{}'::json
    ) author,
    COALESCE(
        (
            SELECT json_build_object('name', s.name, 'eid', se.eid)
            FROM series s
                JOIN eids se ON s.ref_id = se.ref_id
            WHERE s.series_id = b.series_id
        ),
        null
    ) series
FROM books b
    JOIN eids e ON b.ref_id = e.ref_id
WHERE e.eid = :eid;
