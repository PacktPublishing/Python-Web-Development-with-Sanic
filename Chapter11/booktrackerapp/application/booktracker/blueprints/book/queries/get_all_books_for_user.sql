SELECT e.eid,
    b.book_id,
    b.title,
    row_to_json(
        (
            SELECT q
            FROM (
                    SELECT a.name,
                        ae.eid
                    FROM authors a
                        JOIN eids ae ON a.ref_id = ae.ref_id
                    WHERE a.author_id = b.author_id
                ) q
        )
    ) author,
    row_to_json(
        (
            SELECT q
            FROM (
                    SELECT s.name,
                        se.eid
                    FROM series s
                        JOIN eids se ON s.ref_id = se.ref_id
                    WHERE s.series_id = b.series_id
                ) q
        )
    ) series,
    bu.is_loved,
    bu.state
FROM books b
    JOIN eids e ON b.ref_id = e.ref_id
    JOIN book_to_user bu ON b.book_id = bu.book_id
WHERE bu.user_id = :user_id
LIMIT :limit OFFSET :offset;
