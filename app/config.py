import os
from urllib.parse import quote_plus

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurações base."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Se DATABASE_URL estiver definida (por ex. em produção), usa ela.
    database_url_env = os.getenv("DATABASE_URL")
    if database_url_env:
        SQLALCHEMY_DATABASE_URI = database_url_env
    else:
        POSTGRES_USER = os.getenv("POSTGRES_USER", "books_user")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
        POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        POSTGRES_DB = os.getenv("POSTGRES_DB", "books_db")

        # Garantir percent-encoding da senha (e de outros campos se necessário)
        pwd = quote_plus(POSTGRES_PASSWORD)
        SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{pwd}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT (opcional)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))

    JSON_SORT_KEYS = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(Config):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL", "sqlite:///:memory:")
