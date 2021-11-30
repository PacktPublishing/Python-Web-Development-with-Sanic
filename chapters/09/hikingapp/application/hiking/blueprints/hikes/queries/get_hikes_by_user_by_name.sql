SELECT      t.*, h.date
FROM        hikes h
JOIN        trails t ON h.trail_id = t.trail_id
JOIN        users u ON h.user_id = u.user_id
WHERE       LOWER(u.name) = LOWER(:name);
