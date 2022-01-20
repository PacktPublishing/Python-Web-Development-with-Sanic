WITH ref as (
    INSERT INTO eids (eid, type)
    VALUES (:eid, 'authors')
    RETURNING ref_id
)
INSERT INTO authors (ref_id, name)
SELECT ref_id,
    :name
FROM ref
RETURNING author_id,
    name,
    :eid as eid;
