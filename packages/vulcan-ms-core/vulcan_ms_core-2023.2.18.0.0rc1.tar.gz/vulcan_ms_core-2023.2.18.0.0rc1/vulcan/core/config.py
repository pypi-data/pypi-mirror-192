import os
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings

TEMP_DIR = Path(gettempdir())


class Config(BaseSettings):
    APP_NAME: str = "vulcan-fastapi-ms"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 5000
    RELOAD: str = "False"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_DATABASE: str = "app"
    JWT_SECRET_KEY: str = "vulcan-fastapi-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    PROMETHEUS_DIR: Path = TEMP_DIR / "prom"


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    DB_USER: str = "test"
    DB_PASS: str = "test"


class LocalConfig(Config):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    DB_HOST: str = "localhost"
    RELOAD: str = "True"


class ProductionConfig(Config):
    DEBUG: str = False
    LOG_LEVEL: str = "WARN"


def get_config():
    env = os.getenv("ENVIRONMENT", "local")
    if (env is None) or (env not in ["dev", "local", "prod", "test"]):
        raise Exception("Invalid environment. Should be one of: dev, local, prod, test")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config: Config = get_config()
