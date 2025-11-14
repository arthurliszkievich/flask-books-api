# Documentação de API — Resumo (endpoints principais)

Base path: /api

Modelo Book (campos principais)
- id: integer
- title: string (obrigatório)
- author: string (obrigatório)
- isbn: string (13) (opcional / único)
- genre: string (opcional)
- publication_year: integer (opcional)
- description: string (opcional)
- created_at, updated_at: timestamps

Endpoints

1) GET /api/books
- Descrição: Lista todos os livros (adicionar paginação futuramente)
- Exemplo requisição:
  GET /api/books
- Resposta 200:
  [
    {
      "id": 1,
      "title": "1984",
      "author": "George Orwell",
      "isbn": "0451524934",
      "genre": "Dystopia",
      "publication_year": 1949,
      "description": "...",
      "created_at": "2025-11-14T12:00:00",
      "updated_at": null
    }
  ]

2) GET /api/books/{id}
- Descrição: Busca livro por ID
- Resposta 200: objeto Book
- Resposta 404: {"message": "Not Found"} (padrão get_or_404)

3) POST /api/books
- Descrição: Cria novo livro
- Requisição (JSON):
  {
    "title": "O Senhor dos Anéis",
    "author": "J.R.R. Tolkien",
    "isbn": "9780261102385",
    "genre": "Fantasy",
    "publication_year": 1954,
    "description": "..."
  }
- Resposta 201: objeto criado
- Validação mínima: title e author obrigatórios

4) PUT /api/books/{id}
- Descrição: Atualiza campos enviados de um livro
- Requisição (JSON): qualquer campo do modelo
- Resposta 200: objeto atualizado
- Resposta 404: se id não existe

5) DELETE /api/books/{id}
- Descrição: Remove um livro
- Resposta 200: {"message": "Book deleted successfully"}

6) GET /api/health
- Descrição: Health check simples
- Resposta 200: {"status": "healthy"}

Autenticação (planejada)
- Endpoints esperados:
  - POST /api/auth/register
  - POST /api/auth/login
- Fluxo: usuário envia credenciais, recebe access token (JWT), utiliza Authorization: Bearer <token> nas requisições protegidas
- Regras: rotas de criação/atualização/deleção podem ser protegidas por JWT

Erros
- 400 Bad Request → entradas inválidas (body ausente ou inválido)
- 401 Unauthorized → token inválido/ausente (quando autenticado)
- 404 Not Found → recurso não encontrado
- 500 Internal Server Error → erro do servidor (tratar com handlers)

Notas
- Implementar validação explícita (Marshmallow/Pydantic) para respostas consistentes
- Implementar paginação e filtros (ex.: /api/books?author=Tolkien&genre=Fantasy&page=1&page_size=20)