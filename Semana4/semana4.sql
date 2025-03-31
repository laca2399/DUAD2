CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(200) NOT NULL,
    author VARCHAR (25)
);

INSERT INTO books (name, author)
    VALUES ('Don Quijote', 1);

INSERT INTO books (name, author)
    VALUES ('La Divina Comedia', 2);

INSERT INTO books (name, author)
    VALUES ('Vagabond 1-3', 3);

INSERT INTO books (name, author)
    VALUES ('Dragon Ball 1', 4);

INSERT INTO books (name, author)
    VALUES ('The Book of the 5 Rings', NULL);

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(200) NOT NULL
);

INSERT INTO authors (name)
    VALUES ('Miguel de Cervantes');

INSERT INTO authors (name)
    VALUES ('Dante Alighieri');

INSERT INTO authors (name)
    VALUES ('Takehiko Inoue');

INSERT INTO authors (name)
    VALUES ('Akira Toriyama');

INSERT INTO authors (name)
    VALUES ('Walt Disney');

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(200) NOT NULL,
    email TEXT NOT NULL
);

INSERT INTO customers (name, email)
    VALUES ('John Doe', 'j.doe@email.com');

INSERT INTO customers (name, email)
    VALUES ('Jane Doe', 'jane@doe.com');

INSERT INTO customers (name, email)
    VALUES ('Luke Skywalker', 'darth.son@email.com');

CREATE TABLE rents (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    bookid SMALL INT NOT NULL,
    customerid SMALL INT NOT NULL, 
    state VARCHAR (25) NOT NULL
);

INSERT INTO rents (bookid, customerid, state)
    VALUES (1, 2, 'Returned');

INSERT INTO rents (bookid, customerid, state)
    VALUES (2, 2, 'Returned');

INSERT INTO rents (bookid, customerid, state)
    VALUES (1, 1, 'On time');

INSERT INTO rents (bookid, customerid, state)
    VALUES (3, 1, 'On time');

INSERT INTO rents (bookid, customerid, state)
    VALUES (2, 2, 'Overdue');

--Obtenga todos los libros y sus autores
SELECT books.name, authors.name  
FROM books AS books
INNER JOIN authors AS authors
ON books.author = authors.id;

--Obtenga todos los libros que no tienen autor
SELECT books.name
FROM books AS books
LEFT JOIN authors AS authors
ON books.author = authors.id
WHERE books.author IS NULL;

--Obtenga todos los autores que no tienen libros
SELECT authors.name
FROM authors AS authors
LEFT JOIN books AS books
ON authors.id = books.author
WHERE books.author IS NULL;

--Obtenga todos los libros que han sido rentados en algún momento
SELECT DISTINCT books.name  
FROM books AS books
INNER JOIN rents AS rents 
ON books.id = rents.bookid;

--Obtenga todos los libros que nunca han sido rentados
SELECT books.name
FROM books AS books
LEFT JOIN rents AS rents
ON books.id = rents.bookid
WHERE rents.bookid IS NULL;

--Obtenga todos los clientes que nunca han rentado un libro
SELECT customers.name
FROM customers AS customers
LEFT JOIN rents AS rents
ON customers.id = rents.customerid
WHERE rents.customerid IS NULL;

--Obtenga todos los libros que han sido rentados y están en estado “Overdue”
SELECT books.name  
FROM books AS books
INNER JOIN rents AS rents 
ON books.id = rents.bookid
WHERE rents.state = 'Overdue';

