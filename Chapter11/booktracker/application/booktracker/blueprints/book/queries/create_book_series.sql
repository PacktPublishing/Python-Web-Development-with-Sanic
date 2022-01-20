WITH ref as (
    INSERT INTO eids (eid, type)
    VALUES (:eid, 'series')
    RETURNING ref_id
)
INSERT INTO series (ref_id, name)
SELECT ref_id,
    :name
FROM ref
RETURNING series_id,
    name,
    :eid as eid;
