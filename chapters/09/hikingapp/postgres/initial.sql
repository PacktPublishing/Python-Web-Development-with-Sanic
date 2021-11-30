CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(256) NOT NULL
);

CREATE TABLE trails (
    trail_id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(256) NOT NULL,
    distance NUMERIC(6,2) NOT NULL
);

CREATE TABLE hikes (
    trail_id INTEGER REFERENCES trails (trail_id),
    user_id INTEGER REFERENCES users (user_id),
    date DATE,
    PRIMARY KEY (trail_id, user_id)
);


INSERT INTO users (name) VALUES
    ('Alice'),
    ('Bob'),
    ('Carol');

INSERT INTO trails (name, distance) VALUES
    ('Green', 7.7),
    ('Red', 22.4),
    ('Blue', 1025),
    ('White', 613),
    ('Black', 54.1);

INSERT INTO hikes (user_id, trail_id, date) VALUES
    (1, 1, '2021-01-01'),
    (1, 2, '2021-02-01'),
    (2, 5, '2021-05-02'),
    (3, 1, '2021-01-03'),
    (3, 5, '2021-05-03');
