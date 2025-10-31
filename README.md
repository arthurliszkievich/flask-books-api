# 📚 Flask Books API

API REST para gerenciamento de catálogo de livros, construída com Flask e Docker.

## 🎯 Objetivo do Projeto

Este projeto foi criado para aprender:
- Desenvolvimento de APIs REST com Flask
- Containerização com Docker
- Boas práticas de desenvolvimento Python
- Integração com bancos de dados

## 🚀 Funcionalidades

- [ ] Listar todos os livros
- [ ] Buscar livro por ID
- [ ] Adicionar novo livro
- [ ] Atualizar informações de um livro
- [ ] Deletar livro
- [ ] Buscar livros por autor
- [ ] Buscar livros por gênero

## 🛠️ Tecnologias

- Python 3.11+
- Flask
- SQLAlchemy
- Docker
- PostgreSQL (futuro)

## 📦 Como Executar (Local)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python run.py
```

## 🐳 Como Executar (Docker)

```bash
# Construir e executar
docker-compose up --build

# Parar containers
docker-compose down
```

## 📝 Endpoints da API

### Livros

- `GET /api/books` - Lista todos os livros
- `GET /api/books/<id>` - Busca livro por ID
- `POST /api/books` - Adiciona novo livro
- `PUT /api/books/<id>` - Atualiza livro
- `DELETE /api/books/<id>` - Deleta livro

## 📚 Roadmap de Aprendizado

1. ✅ Setup inicial do projeto
2. ⏳ API REST básica com Flask
3. ⏳ Dockerização da aplicação
4. ⏳ Integração com banco de dados
5. ⏳ Testes automatizados
6. ⏳ Features avançadas

## 📖 Recursos de Estudo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [REST API Best Practices](https://restfulapi.net/)

## 👨‍💻 Autor

Arthur Liszkievich