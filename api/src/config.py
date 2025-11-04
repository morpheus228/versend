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
class RedisConfig:
    host: str
    password: str
    user: str
    database: int
    port: int


@dataclass
class AIConfig:
    openai_token: str


@dataclass
class Config:
    mysql: MYSQLConfig
    redis: RedisConfig
    ai: AIConfig

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
        
        cls.redis = RedisConfig(
            host=os.getenv('REDIS_HOST'),
            password=os.getenv('REDIS_PASSWORD'),
            user=os.getenv('REDIS_USER'),
            database=int(os.getenv('REDIS_DATABASE')),
            port=int(os.getenv('REDIS_PORT'))
        )

        cls.ai = AIConfig(
            openai_token=os.getenv('OPENAI_API_KEY')
        )