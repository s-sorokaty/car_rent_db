from dotenv import dotenv_values
from pydantic import BaseModel


config = dotenv_values(".env")

class Config(BaseModel):
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_DB:str


def get_config() -> Config:
    return Config(**config)