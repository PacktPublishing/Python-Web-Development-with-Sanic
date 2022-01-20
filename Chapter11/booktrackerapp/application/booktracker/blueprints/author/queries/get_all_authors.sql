SELECT e.eid,
    a.author_id,
    a.name,
    (
        SELECT count(1)
        FROM books b
        WHERE b.author_id = a.author_id
    ) as num_books
FROM authors a
    JOIN eids e ON a.ref_id = e.ref_id
LIMIT :limit OFFSET :offset;
