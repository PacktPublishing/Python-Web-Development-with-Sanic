WITH ref as (
    INSERT INTO eids (eid, type)
    VALUES (:eid, 'users')
    RETURNING ref_id
)
INSERT INTO users (login, ref_id, name, avatar, profile)
SELECT :login,
    ref_id,
    :name,
    :avatar,
    :profile
FROM ref
RETURNING user_id;
