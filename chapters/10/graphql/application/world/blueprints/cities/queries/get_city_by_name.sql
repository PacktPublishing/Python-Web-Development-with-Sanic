SELECT      *
FROM        city c
WHERE       LOWER(name) = LOWER(:name);
