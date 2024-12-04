-- Crear los schemas para la base de datos, según diseño

CREATE SCHEMA IF NOT EXISTS ms_products;
CREATE SCHEMA IF NOT EXISTS ms_stocks;
CREATE SCHEMA IF NOT EXISTS ms_purchases;
CREATE SCHEMA IF NOT EXISTS ms_payments;

-- Crear las tablas para la base de datos, según diseño

CREATE TABLE IF NOT EXISTS ms_products.products(id_product SERIAL PRIMARY KEY,
								 name VARCHAR(100) NOT NULL,
								 price FLOAT NOT NULL,
								 active BOOLEAN DEFAULT TRUE NOT NULL);

CREATE TABLE IF NOT EXISTS ms_stocks.stocks(id_stock SERIAL PRIMARY KEY,
							id_product INTEGER NOT NULL,
							transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							quantity INTEGER NOT NULL,
							in_out INTEGER NOT NULL,
							active BOOLEAN DEFAULT TRUE NOT NULL);

CREATE TABLE IF NOT EXISTS ms_purchases.purchases(id_purchase SERIAL PRIMARY KEY,
								   id_product INTEGER NOT NULL,
								   purchase_date TIMESTAMP NOT NULL,
								   shipping_address VARCHAR(200) NOT NULL,
								   active BOOL DEFAULT TRUE,
								   deleted BOOL DEFAULT FALSE,
								   CONSTRAINT fk_id_product_purchases
								   FOREIGN KEY (id_product)
								   REFERENCES ms_products.products(id_product));
							
CREATE TABLE IF NOT EXISTS ms_payments.payments(id_payment SERIAL PRIMARY KEY,
								 id_product INTEGER NOT NULL,
								 amount DECIMAL(10,2) NOT NULL,
								 payment_mode VARCHAR(50) NOT NULL,
								 active BOOL DEFAULT TRUE,
								 CONSTRAINT fk_id_product_payments
								   FOREIGN KEY (id_product)
								   REFERENCES ms_products.products(id_product));

-- Poblar la tabla productos
INSERT INTO ms_products.products(name, price) VALUES ('tomates', 2.99);
INSERT INTO ms_products.products(name, price) VALUES ('papa', 3.99);
INSERT INTO ms_products.products(name, price) VALUES ('lechuga', 4.99);
INSERT INTO ms_products.products(name, price) VALUES ('huevos', 15.99);

-- Poblar la tabla stocks
INSERT INTO ms_stocks.stocks(id_product, quantity, in_out) VALUES (2, 50, 1);
INSERT INTO ms_stocks.stocks(id_product, quantity, in_out) VALUES (3, 10, 1);
INSERT INTO ms_stocks.stocks(id_product, quantity, in_out) VALUES (1, 19, 1);
INSERT INTO ms_stocks.stocks(id_product, quantity, in_out) VALUES (4, 13, 1);