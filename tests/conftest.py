import pytest

from app import create_app, db


class TestConfig:
    """Configuração de teste."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes."""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cria um cliente de teste."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Cria um runner para comandos CLI."""
    return app.test_cli_runner()
