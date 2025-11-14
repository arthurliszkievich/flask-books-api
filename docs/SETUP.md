# Setup — executar o projeto (local e Docker)

Pré-requisitos
- Python 3.11+
- Docker & Docker Compose (para execução com containers)
- (Opcional) PostgreSQL se preferir rodar localmente fora do container

Variáveis de ambiente (crie um `.env` usando `.env.example`)
- FLASK_ENV=development
- FLASK_DEBUG=1
- DATABASE_URL=postgresql://user:password@db:5432/books_db
- SECRET_KEY=uma_chave_secreta_mudepra_producao

Executar localmente (modo rápido com SQLite)
1. Criar ambiente virtual:
   python -m venv venv
2. Ativar:
   source venv/bin/activate  (Linux/Mac) ou venv\Scripts\activate (Windows)
3. Instalar dependências:
   pip install -r requirements.txt
4. Definir variáveis (ex.: export DATABASE_URL='sqlite:///books.db')
5. Executar:
   python run.py

Executar com Docker (dev com PostgreSQL)
1. Atualizar `docker-compose.yml` para incluir serviço `db` (Postgres) — exemplo:
   - Eu recomendo criar o serviço `db` (postgres:15), volumes e variáveis de ambiente.
2. Construir e subir:
   docker-compose up --build
3. A API ficará acessível em http://localhost:5000

Exemplo mínimo `docker-compose` (adicionar ao projeto se escolher)
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
    command: python run.py
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: books_user
      POSTGRES_PASSWORD: books_pass
      POSTGRES_DB: books_db
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

Migrations (recomendado)
- Instalar Flask-Migrate:
  pip install Flask-Migrate
- Inicializar (uma vez):
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade

Testes
- Instalar pytest e pytest-flask
- Escrever testes em tests/
- Executar:
  pytest

Observações finais
- Use `.env` para variáveis sensíveis e não envie para o repo.
- Ajustar `requirements.txt` para incluir as libs necessárias (Flask-JWT-Extended, Flask-Migrate, psycopg2-binary, etc.).