import logging

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from app.utils.wait_for_db import wait_for_db

db = SQLAlchemy()
migrate = Migrate()

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


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

    # Registrar error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {str(error)}")
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

    return app
