SELECT      t.*, h.date
FROM        hikes h
JOIN        trails t ON h.trail_id = t.trail_id
WHERE       h.user_id = :user_id
