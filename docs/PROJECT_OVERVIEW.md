# Projeto: Flask Books API — Visão Geral

Descrição
- API REST para gerenciar catálogo de livros (CRUD), pensada como projeto de portfólio.
- Objetivos: aprender Flask, organização de projeto, containerização (Docker), banco relacional, autenticação JWT, documentação Swagger/OpenAPI e testes automatizados.

Principais funcionalidades
- CRUD de livros (título, autor, isbn, gênero, ano, descrição)
- Endpoints públicos e — futuramente — endpoints protegidos por autenticação (usuários, tokens JWT)
- Health-check
- Busca e filtros (por autor, gênero)
- Paginação para listagens grandes
- Docker + Docker Compose para ambiente de desenvolvimento
- Documentação interativa via Swagger/OpenAPI

Público-alvo
- Recrutadores / avaliadores técnicos
- Você (para aprendizado e demonstração técnica)

Stack técnico
- Python 3.11, Flask 3.x
- Flask-SQLAlchemy (ORM)
- PostgreSQL (produção/dev com Docker)
- Docker + Docker Compose
- (planejado) Flask-JWT-Extended, Flask-Migrate, Flask-RESTX ou flask-smorest, Marshmallow ou Pydantic
- Testes: pytest + pytest-flask

Estado atual (resumo)
- Base funcional com: app/__init__.py (application factory), app/models.py (Book), app/routes.py (endpoints CRUD e health), Dockerfile, docker-compose.yml, README.md básico.
- Falta: app/config.py, run.py (se for preciso revisar), autenticação JWT, documentação Swagger implementada, migrations e testes.

Objetivos do roadmap (curto/médio prazo)
1. Criar app/config.py e .env.example
2. Integrar PostgreSQL no docker-compose para dev
3. Adicionar Flask-Migrate e gerar migração inicial
4. Implementar autenticação JWT (register/login) e proteger rotas
5. Documentar API com OpenAPI/Swagger e publicar UI
6. Adicionar validação de entrada (Marshmallow ou Pydantic)
7. Escrever testes (pytest) e configurar CI (GitHub Actions)
8. Refinar Dockerfile (multi-stage) e adicionar gunicorn para produção

Observações
- Para protótipo, db.create_all() é suficiente; para evolução profissional, usar migrações.
- Documentação e autenticação aumentam muito o valor do portfólio.