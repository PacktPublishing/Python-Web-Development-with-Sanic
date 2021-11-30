SELECT      *,
            (
                SELECT      SUM(distance)
                FROM        trails t
                JOIN        hikes h on t.trail_id = h.trail_id
                WHERE       h.user_id = u.user_id
            ) total_distance_hiked
FROM        users u
WHERE       LOWER(name) = LOWER(:name);
