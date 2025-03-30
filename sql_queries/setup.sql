-- Customers Table
CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    country VARCHAR(50)
);

INSERT INTO Customers (customer_id, name, email, phone, address)
VALUES
    (1, 'ABC Corp', 'contact@abccorp.com', '+1-555-1010', 'New York, USA'),
    (2, 'XYZ Ltd', 'info@xyzltd.com', '+44-20-1234-5678', 'London, UK'),
    (3, 'Green Energy Inc', 'sales@greenenergy.com', '+33-1-2345-6789', 'Paris, France'),
    (4, 'Power Solutions', 'contact@powersolutions.com', '+49-30-9876-5432', 'Berlin, Germany'),
    (5, 'SolarTech', 'hello@solartech.com', '+34-91-6543-210', 'Madrid, Spain');

-- Products Table
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50)
);

INSERT INTO Products (product_id, name, category, price)
VALUES
    (1, 'Circuit Breaker', 'Electrical', 100),
    (2, 'Transformer', 'Electrical', 500),
    (3, 'Solar Inverter', 'Renewable Energy', 1200),
    (4, 'Battery Storage', 'Renewable Energy', 800),
    (5, 'Smart Meter', 'IoT', 300),
    (6, 'Industrial Switchgear', 'Electrical', 700);

-- Orders Table
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP,  -- Added delivery date
    status VARCHAR(20) CHECK (status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled'))
);


INSERT INTO Orders (order_id, customer_id, order_date, delivery_date, status)
VALUES
    (101, 1, '2025-02-15', '2025-02-20', 'Delivered'),
    (102, 2, '2025-02-20', NULL, 'Shipped'), -- No delivery date yet
    (103, 3, '2025-01-21', '2025-01-30', 'Delivered'),
    (104, 4, '2025-03-05', NULL, 'Cancelled'), -- Cancelled orders don't get delivered
    (105, 5, '2025-03-10', NULL, 'Pending'), -- Pending orders don't have a delivery date
    (106, 1, '2025-02-28', '2025-03-07', 'Delivered'),
    (107, 3, '2025-03-01', '2025-03-03', 'Delivered'),
    (108, 2, '2025-03-07', NULL, 'Shipped'), -- No delivery date yet
    (109, 5, '2025-02-25', '2025-03-01', 'Delivered');


-- OrderDetails Table
CREATE TABLE OrderDetails (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    total_price DECIMAL(10,2) NOT NULL
);

INSERT INTO OrderDetails (order_detail_id, order_id, product_id, quantity, total_price)
VALUES
    (1, 101, 1, 10, 750),  
    (2, 101, 2, 5, 2500),  
    (3, 102, 3, 2, 2350),  
    (4, 103, 4, 4, 3200),  
    (5, 104, 5, 6, 1800),  
    (6, 105, 6, 3, 2100),  
    (7, 106, 1, 15, 1000),  
    (8, 107, 2, 2, 1000),  
    (9, 108, 3, 1, 1200),  
    (10, 109, 5, 2, 500);

-- Inventory Table
CREATE TABLE Inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Products(product_id),
    warehouse_location VARCHAR(100),
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0)
);

INSERT INTO Inventory (inventory_id, product_id, warehouse_location, stock_quantity)
VALUES
    (1, 1, 'New York Warehouse', 500),
    (2, 2, 'London Warehouse', 30),
    (3, 3, 'Paris Warehouse', 150),
    (4, 4, 'Berlin Warehouse', 200),
    (5, 5, 'Madrid Warehouse', 250),
    (6, 6, 'New York Warehouse', 10),
    (7, 2, 'New York Warehouse', 500),
    (8,3, 'London Warehouse', 300),
    (9, 4, 'Paris Warehouse', 10),
    (10, 5, 'Berlin Warehouse', 200),
    (11, 6, 'Madrid Warehouse', 20),
    (12, 1, 'New York Warehouse', 100),
    (13, 3, 'New York Warehouse', 500),
    (14, 4, 'London Warehouse', 300),
    (15, 5, 'Paris Warehouse', 10),
    (16, 6, 'Berlin Warehouse', 200),
    (17, 1, 'Madrid Warehouse', 20),
    (18, 2, 'New York Warehouse', 100);