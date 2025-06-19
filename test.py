import pytest
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.db_repository import engine

# Настройки подключения к базе данных
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    pass

def test_add_car(setup_database):
    with Session() as session:
        session.execute(text("SELECT add_car('Toyota', 'Camry', 2020, 50.00);"))
        result = session.execute(text("SELECT COUNT(*) FROM Cars;")).scalar()
        assert result == 1
        

def test_add_customer(setup_database):
    with Session() as session:
        session.execute(text("SELECT add_customer('John', 'Doe', 'john.doe@example.com', '1234567890');"))
        result = session.execute(text("SELECT COUNT(*) FROM Customers;")).scalar()
        assert result == 1

def test_rent_car(setup_database):
    with Session() as session:
        # Добавляем автомобиль и клиента для теста
        session.execute(text("SELECT add_car('Honda', 'Civic', 2021, 45.00);"))
        session.execute(text("SELECT add_customer('Alice', 'Smith', 'alice.smith@example.com', '9876543210');"))
        
        # Получаем ID автомобиля и клиента
        car_id = session.execute(text("SELECT id FROM Cars WHERE make = 'Honda' AND model = 'Civic';")).scalar()
        customer_id = session.execute(text("SELECT id FROM Customers WHERE email = 'alice.smith@example.com';")).scalar()

        # Арендуем автомобиль, передавая даты в формате date
        start_date = datetime(2025, 6, 20).date()  # Изменено на .date()
        end_date = datetime(2025, 6, 25).date()    # Изменено на .date()

        session.execute(text("SELECT rent_car(:car_id, :customer_id, :start_date, :end_date);"),
                       {"car_id": car_id, "customer_id": customer_id, 
                        "start_date": start_date, "end_date": end_date})

        # Проверяем, что аренда была добавлена
        result = session.execute(text("SELECT COUNT(*) FROM Rentals;")).scalar()
        assert result == 1

        # Проверяем, что автомобиль стал недоступным
        availability = session.execute(text("SELECT available FROM Cars WHERE id = :car_id;"),
                                       {"car_id": car_id}).scalar()
        assert availability is False