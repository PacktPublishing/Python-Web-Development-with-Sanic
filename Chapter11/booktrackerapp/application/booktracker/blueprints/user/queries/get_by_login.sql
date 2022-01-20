SELECT e.eid,
    u.user_id,
    u.login,
    u.name,
    u.avatar,
    u.profile
FROM users u
    JOIN eids e ON u.ref_id = e.ref_id
WHERE u.login = :login;
