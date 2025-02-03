-- Customers Table
CREATE TABLE customer_details (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

-- Orders Table
CREATE TABLE order_details (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(50),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_timestamp TIMESTAMP,
    order_estimated_delivery_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customer_details(customer_id)
);

-- Products Table
CREATE TABLE product_details (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

-- Payments Table (Fix FK)
CREATE TABLE payment_details (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC(10,2),
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES order_details(order_id) ON DELETE CASCADE
);

-- Order Items Table (Fix FK Constraints)
CREATE TABLE orderitem_details (
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    price NUMERIC(10,2),
    shipping_charges NUMERIC(10,2),
    PRIMARY KEY (order_id, product_id, seller_id),
    FOREIGN KEY (order_id) REFERENCES order_details(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product_details(product_id) ON DELETE CASCADE
);
