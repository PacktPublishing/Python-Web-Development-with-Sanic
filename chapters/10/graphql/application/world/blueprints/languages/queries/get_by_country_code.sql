SELECT      *
FROM        countrylanguage
WHERE       countrycode = :country_code
LIMIT       :limit
OFFSET      :offset;
