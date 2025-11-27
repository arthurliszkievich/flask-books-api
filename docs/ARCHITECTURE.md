# Arquitetura do Projeto

Visão geral dos componentes
- Cliente (Postman, navegador, frontend) → faz requisições HTTP
- API (Flask) → Recebe requisições, aplica lógica, acessa DB, retorna JSON
  - app/__init__.py: application factory, registro de blueprints e inicialização de extensões
  - app/routes.py: endpoints (blueprint /api)
  - app/models.py: modelos SQLAlchemy (Book, futuro: User, Loan)
  - app/config.py: configurações por ambiente (dev/prod/test)
- Banco de Dados (SQLite local / PostgreSQL via Docker)
- Docker + Docker Compose → orquestra web + db
- Optional: Swagger UI (servir docs), Admin/pgAdmin, GitHub Actions (CI)

Fluxo de requisição (exemplo GET /api/books)
1. Cliente → GET /api/books
2. Flask router (blueprint) encaminha para função get_books em routes.py
3. Função consulta Book.query (via SQLAlchemy + db.session)
4. Objeto/série de objetos transformados em dicts e retornados como JSON
5. Cliente recebe JSON e status 200

Componentes e responsabilidades
- app/__init__.py
  - Cria app via create_app()
  - Inicializa extensões (db.init_app)
  - Registra blueprints
  - Cria contexto e (temporariamente) db.create_all() para protótipo
- app/models.py
  - Define Book e, no futuro, User, Loan
- app/routes.py
  - Handlers para endpoints CRUD, validação simples, commits/rollbacks
- Database layer
  - Dev: SQLite (fácil de usar)
  - Prod/Dev avançado: PostgreSQL
- Infra via Docker
  - Dockerfile: define imagem da aplicação
  - docker-compose.yml: orquestra containers (web, db)

Considerações de escalabilidade e segurança
- Autenticação: JWT para proteger rotas (login/register endpoints)
- Limitação de carga: adicionar paginação e limites de resultado
- Migrations: usar Flask-Migrate (Alembic) para evoluir schema corretamente
- Logs e monitoramento: expor /metrics (opcional) e configurar logging