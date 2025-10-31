import os
from pathlib import Path

basedir = Path(__file__).parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or f"sqlite:///{basedir / 'books.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
