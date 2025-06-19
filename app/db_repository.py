from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError

from config import get_config

settings = get_config()

db_connect_key = f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{db_connect_key}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Проверка существования базы данных
database_name = settings.POSTGRES_DB

with engine.connect() as connection:
    connection.execute(text("commit"))  # Необходимо для PostgreSQL
    try:
        # Проверяем, существует ли база данных
        res = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname = :db_name"), {"db_name": database_name})
        if len(res.fetchall()) != 0:
            print(f"DB '{database_name}' already exist.")
        else: 
            connection.execute(text(f"CREATE DATABASE {database_name}"))
            print(f"DB '{database_name}' created.")

    except OperationalError as e:
        print(f"Ошибка подключения: {e}")

# Обновляем URL для подключения к новой базе данных
SQLALCHEMY_DATABASE_URL += database_name

# Создаем новый движок для работы с новой базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()