# Guia de Configuração e Testes - Flask Books API

## 📋 Passo a Passo

### 1️⃣ Reconstruir o Container Docker
```powershell
docker-compose down
docker-compose build --no-cache web
docker-compose up -d
```

### 2️⃣ Inicializar Flask-Migrate (Primeira vez)
```powershell
# Entrar no container
docker-compose exec web bash

# Dentro do container, executar:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Sair do container
exit
```

### 3️⃣ Teste Manual - Criar um Livro (curl)
```powershell
# PowerShell (método 1)
Invoke-RestMethod -Uri "http://localhost:5000/api/books" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"title":"Duna","author":"Frank Herbert","isbn":"9780441172719","genre":"Ficção Científica","publication_year":1965}'

# PowerShell (método 2 - mais legível)
$body = @{
    title = "1984"
    author = "George Orwell"
    isbn = "9780451524935"
    genre = "Distopia"
    publication_year = 1949
    description = "Um clássico da literatura distópica"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/books" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### 4️⃣ Verificar Livros Criados
```powershell
# Listar todos os livros
Invoke-RestMethod -Uri "http://localhost:5000/api/books" -Method GET

# Buscar livro específico por ID
Invoke-RestMethod -Uri "http://localhost:5000/api/books/1" -Method GET
```

### 5️⃣ Instalar Dependências no Ambiente Local (Opcional)
```powershell
# Ativar ambiente virtual
& C:/Users/arthu/AProgramação/flask-books-api/venv/Scripts/Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 6️⃣ Executar Testes Pytest
```powershell
# Opção 1: Executar testes no container Docker
docker-compose exec web pytest tests/ -v

# Opção 2: Executar testes localmente (precisa ter dependências instaladas)
pytest tests/ -v

# Executar testes com coverage
pytest tests/ -v --cov=app --cov-report=html

# Executar teste específico
pytest tests/test_create_book.py -v
pytest tests/test_health.py -v
```

## 🔍 Comandos Úteis

### Ver Logs
```powershell
# Ver logs em tempo real
docker-compose logs -f web

# Ver logs do banco de dados
docker-compose logs -f db

# Ver últimas linhas
docker-compose logs --tail=50 web
```

### Gerenciar Containers
```powershell
# Parar containers
docker-compose stop

# Iniciar containers
docker-compose start

# Reiniciar containers
docker-compose restart

# Remover tudo (incluindo volumes)
docker-compose down -v
```

### Migrações do Banco de Dados
```powershell
# Criar nova migração após alterar models
docker-compose exec web flask db migrate -m "Descrição da mudança"

# Aplicar migrações
docker-compose exec web flask db upgrade

# Reverter última migração
docker-compose exec web flask db downgrade

# Ver histórico de migrações
docker-compose exec web flask db history

# Ver status atual
docker-compose exec web flask db current
```

### Acessar Banco de Dados Diretamente
```powershell
# Entrar no PostgreSQL
docker-compose exec db psql -U books_user -d books_db

# Comandos úteis dentro do psql:
# \dt              - Listar tabelas
# \d books         - Descrever tabela books
# SELECT * FROM books;  - Ver todos os livros
# \q               - Sair
```

## 🧪 Estrutura de Testes Criada

### tests/conftest.py
- Fixtures do pytest
- Configuração do app de teste
- Cliente de teste

### tests/test_health.py
- Teste de health check da API
- Verifica se endpoint /api/books responde

### tests/test_create_book.py
- Teste de criação de livro
- Teste de validação de campos obrigatórios
- Teste de recuperação de livro criado

## 📁 Arquivos Criados/Modificados

✅ app/utils/__init__.py (novo)
✅ app/utils/wait_for_db.py (novo)
✅ app/__init__.py (atualizado com Flask-Migrate)
✅ tests/conftest.py (novo)
✅ tests/test_health.py (novo)
✅ tests/test_create_book.py (novo)
✅ requirements.txt (atualizado com pytest)

## 🎯 Próximos Passos

1. Execute os comandos na ordem apresentada
2. Cole aqui qualquer erro que aparecer
3. Execute os testes e compartilhe os resultados
4. Se tudo funcionar, podemos adicionar mais funcionalidades!

## ❗ Troubleshooting

### Erro: "No module named 'flask_migrate'"
```powershell
docker-compose build --no-cache web
docker-compose up -d
```

### Erro: "could not translate host name"
- Verifique se o arquivo .env está correto
- Confirme que DATABASE_URL não tem caracteres especiais sem encoding

### Erro: "Connection refused"
- Aguarde alguns segundos para o banco inicializar
- O wait_for_db agora cuida disso automaticamente

### Testes falhando
```powershell
# Limpar tudo e reconstruir
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```
