WITH ref as (
    INSERT INTO eids (eid, type)
    VALUES (:eid, 'books')
    RETURNING ref_id
)
INSERT INTO books (ref_id, title, author_id, series_id)
SELECT ref_id,
    :title,
    :author_id,
    :series_id
FROM ref
RETURNING book_id;
