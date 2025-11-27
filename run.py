import os

from app import create_app

# Cria a aplicação usando a factory (app/__init__.py)
app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    # Usa DEBUG a partir da config carregada
    debug = app.config.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)
