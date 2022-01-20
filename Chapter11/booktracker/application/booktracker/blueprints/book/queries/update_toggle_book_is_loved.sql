UPDATE book_to_user bu
SET is_loved = NOT bu.is_loved
FROM (
        SELECT book_id
        FROM books b
            JOIN eids e ON b.ref_id = e.ref_id
        WHERE e.eid = :eid
    ) q
WHERE bu.book_id = q.book_id
    AND bu.user_id = :user_id;
