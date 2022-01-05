SELECT      *
FROM        city
WHERE       countrycode = :code
LIMIT       :limit
OFFSET      :offset;
