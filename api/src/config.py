from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass
class MYSQLConfig:
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class AIConfig:
    openai_token: str


@dataclass
class APIConfig:
    host: str
    port: str


@dataclass
class FrontConfig:
    host: str
    port: str


@dataclass
class Config:
    mysql: MYSQLConfig
    ai: AIConfig
    api: APIConfig
    front: FrontConfig

    @classmethod
    def set(cls, path: str = '.env'):
        load_dotenv(path)

        cls.mysql = MYSQLConfig(
            host=os.getenv('MYSQL_HOST'),
            password=os.getenv('MYSQL_PASSWORD'),
            user=os.getenv('MYSQL_USER'),
            database=os.getenv('MYSQL_DATABASE'),
            port=os.getenv('MYSQL_PORT')
        )

        cls.ai = AIConfig(
            openai_token=os.getenv('OPENAI_API_KEY')
        )

        cls.api = APIConfig(
            host = os.getenv('API_HOST'),
            port = os.getenv('API_PORT')
        )

        cls.front = FrontConfig(
            host = os.getenv('FRONT_HOST'),
            port = os.getenv('FRONT_PORT')
        )