from sqlalchemy import text

from app.db_repository import engine
from alembic import op


functions = """
CREATE OR REPLACE FUNCTION add_car(
    p_make VARCHAR,
    p_model VARCHAR,
    p_year INT,
    p_price_per_day DECIMAL
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Cars (make, model, year, price_per_day, available)
    VALUES (p_make, p_model, p_year, p_price_per_day, TRUE);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_customer(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_email VARCHAR,
    p_phone VARCHAR
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Customers (first_name, last_name, email, phone)
    VALUES (p_first_name, p_last_name, p_email, p_phone);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION rent_car(
    p_car_id INT,
    p_customer_id INT,
    p_start_date DATE,
    p_end_date DATE
) RETURNS VOID AS $$
DECLARE
    v_price DECIMAL;
    v_total_days INT;
BEGIN
    SELECT price_per_day INTO v_price FROM Cars WHERE id = p_car_id;
    IF v_price IS NULL OR NOT EXISTS (SELECT 1 FROM Cars WHERE id = p_car_id AND available) THEN
        RAISE EXCEPTION 'Car not available for rent';
    END IF;
    v_total_days := (p_end_date - p_start_date);
    INSERT INTO Rentals (car_id, customer_id, start_date, end_date, total_price)
    VALUES (p_car_id, p_customer_id, p_start_date, p_end_date, v_price * v_total_days);
    UPDATE Cars SET available = FALSE WHERE id = p_car_id;
END;
$$ LANGUAGE plpgsql;
"""

def add_car(make, model, year, price_per_day):
    with engine.connect() as connection:
        connection.execute(text("SELECT add_car(:make, :model, :year, :price_per_day)"),
                           {"make": make, "model": model, "year": year, "price_per_day": price_per_day})

def add_customer(first_name, last_name, email, phone):
    with engine.connect() as connection:
        connection.execute(text("SELECT add_customer(:first_name, :last_name, :email, :phone)"),
                           {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone})

def rent_car(car_id, customer_id, start_date, end_date):
    with engine.connect() as connection:
        connection.execute(text("SELECT rent_car(:car_id, :customer_id, :start_date, :end_date)"),
                           {"car_id": car_id, "customer_id": customer_id, "start_date": start_date, "end_date": end_date})