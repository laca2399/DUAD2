--TABLE CREATION

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    code SMALLINT UNIQUE NOT NULL,
    name VARCHAR(25) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    entry_date TEXT DEFAULT '2025-01-12 00:00:00',
    branch VARCHAR(25) NOT NULL
);

CREATE TABLE invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    invoice_number SMALLINT UNIQUE NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payer_email TEXT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payer_phone_number VARCHAR(20) NOT NULL,
    employee_code VARCHAR(20) NOT NULL
);

CREATE TABLE cart(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payer_email TEXT FK REFERENCES invoice(payer_email)
);

CREATE TABLE invoice_product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number SMALLINT FK REFERENCES invoice (invoice_number),
    product_code SMALLINT FK REFERENCES product(code)
    quantity_purchased SMALLINT NOT NULL,
    total_amount DECIMAL (10,2) NOT NULL
);

CREATE TABLE cart_product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INT FK REFERENCES cart(id),
    product_code SMALLINT FK REFERENCES product(code),
    quantity SMALLINT NOT NULL
);

--Insert data into product table
INSERT INTO product (code, name, price, branch)
    VALUES (2345, 'table', 300.35, 'HomeTrends')

INSERT INTO product (code, name, price, branch)
    VALUES (1111, 'Ball', 20, 'UEFA')

INSERT INTO product (code, name, price, branch)
    VALUES (3833, 'Laptop', 855, 'HP')

INSERT INTO product (code, name, price, branch)
    VALUES (4250, 'PS5', 499.95, 'Sony')

INSERT INTO product (code, name, price, branch)
    VALUES (7645, 'Lantern', 120.5, 'Flic')

INSERT INTO product (code, name, price, branch)
    VALUES (9120, 'AirFryer', 180.37, 'Ninja')

INSERT INTO product (code, name, price, branch)
    VALUES (264, 'Tesla', 85000, 'Musk');

INSERT INTO product (code, name, price, branch)
    VALUES (762, 'Rocket House', 1250000.65, 'Nasa');

--Insert data into invoice table
INSERT INTO invoice (invoice_number, payer_email, total_amount, payer_phone_number, employee_code)
    VALUES(15964, 'rob.brenes@gmail.com', 200, '76453289', 123);

INSERT INTO invoice (invoice_number, payer_email, total_amount, payer_phone_number, employee_code)
    VALUES(23668, 'tom.gamboa@gmail.com', 400, '88888866', 456);

INSERT INTO invoice (invoice_number, payer_email, total_amount, payer_phone_number, employee_code)
    VALUES(11945, 'gam.gimenez@gmail.com', 100, '44224422', 135);

INSERT INTO invoice (invoice_number, payer_email, total_amount, payer_phone_number, employee_code)
    VALUES(27665, 'sher.holmes@gmail.com', 60, '1509872689', 246);

INSERT INTO invoice (invoice_number, payer_email, total_amount, payer_phone_number, employee_code)
    VALUES(22334, 'andy.ronaldo@gmail.com', 1000, '86542537', 369);

INSERT INTO invoice (invoice_number, payer_email, total_amount, payer_phone_number, employee_code)
    VALUES(12, 'jim.nico@gmail.com', 627.25, '65289347', 158);

--Insert data into cart table
INSERT INTO cart (payer_email)
VALUES ('rob.brenes@gmail.com');

INSERT INTO cart (payer_email)
VALUES ('tom.gamboa@gmail.com');

INSERT INTO cart (payer_email)
VALUES ('gam.gimenez@gmail.com');

INSERT INTO cart (payer_email)
VALUES ('sher.holmes@gmail.com');

INSERT INTO cart (payer_email)
VALUES ('andy.ronaldo@gmail.com');

INSERT INTO cart (payer_email)
VALUES ('jim.nico@gmail.com');

--Insert data into invoice_product table
INSERT INTO invoice_product (invoice_number, product_code, quantity_purchased, total_amount)
VALUES (15964, 2345, 2, 600.70);

INSERT INTO invoice_product (invoice_number, product_code, quantity_purchased, total_amount)
VALUES (23668, 1111, 3, 60.00);

INSERT INTO invoice_product (invoice_number, product_code, quantity_purchased, total_amount)
VALUES (11945, 3833, 1, 855.00);

INSERT INTO invoice_product (invoice_number, product_code, quantity_purchased, total_amount)
VALUES (27665, 4250, 1, 499.95);

INSERT INTO invoice_product (invoice_number, product_code, quantity_purchased, total_amount)
VALUES (22334, 7645, 4, 482.00);

INSERT INTO invoice_product (invoice_number, product_code, quantity_purchased, total_amount)
VALUES (12, 9120, 1, 180.37);

--Insert data into cart_product table
INSERT INTO cart_product (cart_id, product_code, quantity)
VALUES (1, 2345, 2);

INSERT INTO cart_product (cart_id, product_code, quantity)
VALUES (2, 1111, 3);

INSERT INTO cart_product (cart_id, product_code, quantity)
VALUES (3, 3833, 1);

INSERT INTO cart_product (cart_id, product_code, quantity)
VALUES (1, 4250, 1);

INSERT INTO cart_product (cart_id, product_code, quantity)
VALUES (4, 7645, 5);

INSERT INTO cart_product (cart_id, product_code, quantity)
VALUES (5, 9120, 2);

--a. Get all stored products
SELECT *
    FROM product;

--b. Get all products that are priced over 50000
SELECT *
    FROM product
    WHERE price > 50000;

--c. Get all purchases of the same product by ID.
SELECT * 
FROM invoice_product 
WHERE product_code = 2345; --using product_code instead of id
--2nd way using id
SELECT * 
FROM invoice_product 
WHERE product_code = (SELECT code FROM product WHERE id = 1);

--d. Get all purchases grouped by product, showing the total purchased across all purchases.
SELECT product_code, SUM(quantity_purchased) AS total_purchased
FROM invoice_product
GROUP BY product_code
ORDER BY total_purchased DESC;


--e. Get all invoices made by the same buyer
SELECT *
FROM invoice
WHERE payer_email = 'rob.brenes@gmail.com';

--f. Get all invoices sorted by total amount in descending order
SELECT *
FROM invoice
ORDER BY total_amount DESC;

--g. Get a single invoice per invoice number.
SELECT *
FROM invoice
WHERE invoice_number = 15964;
