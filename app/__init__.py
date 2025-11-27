from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.utils.wait_for_db import wait_for_db

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object=None):
    """
    Factory function para criar instância da aplicação Flask.

    Args:
        config_object: Objeto de configuração (padrão: app.config.Config)
                      Pode ser uma string ou um objeto de configuração.
                      Útil para testes (passar configuração de teste).

    Returns:
        app: Instância configurada do Flask
    """
    app = Flask(__name__)

    # Carrega configuração
    if config_object is None:
        app.config.from_object("app.config.Config")
    else:
        app.config.from_object(config_object)

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Aguarda o banco de dados estar disponível (apenas em produção/desenvolvimento)
    if not app.config.get("TESTING", False):
        wait_for_db(db, app)

    with app.app_context():
        from app import routes

        app.register_blueprint(routes.bp)

        # Cria tabelas se não existirem (para ambientes sem migrações)
        db.create_all()

    return app
