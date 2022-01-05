SELECT      *
FROM        trails
WHERE       LOWER(name) = LOWER(:name);
