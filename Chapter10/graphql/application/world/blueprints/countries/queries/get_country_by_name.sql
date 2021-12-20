SELECT      *
FROM        country c
WHERE       LOWER(name) = LOWER(:name);
