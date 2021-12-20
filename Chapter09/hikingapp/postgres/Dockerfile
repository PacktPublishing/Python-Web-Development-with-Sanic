FROM postgres
WORKDIR /docker-entrypoint-initdb.d
ADD initial.sql /docker-entrypoint-initdb.d
EXPOSE 5432
CMD ["postgres", "-c", "log_statement=all", "-c", "log_destination=stderr"]
