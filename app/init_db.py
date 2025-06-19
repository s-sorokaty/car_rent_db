import sqlalchemy
from config import get_config

from app.db_repository import engine

def init():
    try:
        config = get_config()
        schema_name = config.POSTGRES_DB

        # Получаем соединение
        with engine.connect() as connection:
            # Проверяем наличие схемы
            if not connection.dialect.has_schema(connection, schema_name):
                connection.execute(sqlalchemy.schema.CreateSchema(schema_name))
        
        print("DB inited")
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"DB init error: {e}")