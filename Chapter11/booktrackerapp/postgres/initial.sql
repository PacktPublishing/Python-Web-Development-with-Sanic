CREATE EXTENSION pg_trgm;
CREATE TYPE book_state AS ENUM ('read', 'reading', 'unread');
CREATE TABLE eids (
    ref_id SERIAL PRIMARY KEY,
    type CHARACTER VARYING(30) NOT NULL,
    eid CHARACTER (24) NOT NULL UNIQUE
);
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    ref_id INTEGER REFERENCES eids (ref_id) NOT NULL,
    login CHARACTER VARYING(100) NOT NULL,
    name CHARACTER VARYING(100),
    avatar CHARACTER VARYING(100),
    profile CHARACTER VARYING(100)
);
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    ref_id INTEGER REFERENCES eids (ref_id) NOT NULL,
    name CHARACTER VARYING(100) NOT NULL
);
CREATE TABLE series (
    series_id SERIAL PRIMARY KEY,
    ref_id INTEGER REFERENCES eids (ref_id) NOT NULL,
    name CHARACTER VARYING(100) NOT NULL
);
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    ref_id INTEGER REFERENCES eids (ref_id) NOT NULL,
    title CHARACTER VARYING(100) NOT NULL,
    author_id INTEGER REFERENCES authors (author_id) NOT NULL,
    series_id INTEGER REFERENCES series (series_id)
);
CREATE TABLE book_to_user (
    book_id INTEGER REFERENCES books (book_id) NOT NULL,
    user_id INTEGER REFERENCES users (user_id) NOT NULL,
    is_loved BOOLEAN DEFAULT false,
    state book_state DEFAULT 'unread',
    PRIMARY KEY (book_id, user_id)
);
INSERT INTO eids (eid, type)
VALUES ('xxdlvO0xjwsrUbooypcZwkJl', 'authors'),
    ('xxdMkXiurxTKkZaiWNJs3F0D', 'books');
INSERT INTO authors (ref_id, name)
VALUES (1, 'Adam Hopkins');
INSERT INTO books (ref_id, title, author_id)
VALUES (2, 'Python Web Development with Sanic', 1);
