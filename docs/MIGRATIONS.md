# 🗄️ Guia de Migrações com Flask-Migrate

## 📋 O que são Migrações?

Migrações são uma forma de versionar o schema do banco de dados, permitindo:
- Evoluir o banco de forma controlada
- Histórico de todas as mudanças
- Rollback para versões anteriores
- Sincronizar schema entre ambientes (dev, staging, prod)

## 🚀 Inicialização (Primeira Vez)

### **Passo 1: Entrar no Container**
```bash
docker-compose up -d
docker-compose exec web bash
```

### **Passo 2: Inicializar Flask-Migrate**
```bash
# Dentro do container
flask db init
```

Isso cria a pasta `migrations/` com estrutura:
```
migrations/
├── alembic.ini
├── env.py
├── README
├── script.py.mako
└── versions/
```

### **Passo 3: Gerar Migração Inicial**
```bash
flask db migrate -m "Criar tabela books inicial"
```

Isso cria um arquivo em `migrations/versions/` como:
```
migrations/versions/abc123_criar_tabela_books_inicial.py
```

### **Passo 4: Aplicar Migração**
```bash
flask db upgrade
```

### **Passo 5: Verificar**
```bash
flask db current
```

## 🔄 Workflow Normal

### **Quando modificar um modelo:**

1. **Editar o modelo** em `app/models.py`:
```python
class Book(db.Model):
    # ... campos existentes ...
    rating = db.Column(db.Float, nullable=True)  # Novo campo
```

2. **Gerar migração**:
```bash
docker-compose exec web flask db migrate -m "adicionar campo rating"
```

3. **Revisar o arquivo gerado** em `migrations/versions/`:
```python
def upgrade():
    op.add_column('books', sa.Column('rating', sa.Float(), nullable=True))

def downgrade():
    op.drop_column('books', 'rating')
```

4. **Aplicar migração**:
```bash
docker-compose exec web flask db upgrade
```

## 📚 Comandos Importantes

```bash
# Ver histórico completo
flask db history

# Ver migração atual
flask db current

# Aplicar todas as migrações pendentes
flask db upgrade

# Aplicar próxima migração
flask db upgrade +1

# Reverter última migração
flask db downgrade

# Reverter para versão específica
flask db downgrade abc123

# Ver SQL que será executado (sem executar)
flask db upgrade --sql

# Criar migração vazia (para scripts customizados)
flask db revision -m "minha migração custom"
```

## ⚠️ Boas Práticas

### ✅ **FAÇA:**

1. **Sempre revise migrações geradas** antes de aplicar
2. **Teste migrações em dev** antes de produção
3. **Commit das migrações** no repositório
4. **Mensagens descritivas**: `"adicionar índice em email"` não `"mudança"`
5. **Migrações pequenas e atômicas**: uma mudança = uma migração
6. **Backup antes de migrar** em produção

### ❌ **NÃO FAÇA:**

1. **Editar migrações já aplicadas** em outros ambientes
2. **Deletar pasta migrations/** (perde histórico)
3. **Aplicar migrações manualmente** no banco
4. **Fazer rollback em produção** sem testar antes
5. **Misturar mudanças de schema** com mudanças de dados

## 🔐 Migrações com Dados

Às vezes precisa migrar dados junto com schema:

```python
# migrations/versions/xyz789_migrar_dados.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 1. Adicionar coluna
    op.add_column('books', sa.Column('status', sa.String(20), nullable=True))
    
    # 2. Popular com dados padrão
    op.execute("UPDATE books SET status = 'available'")
    
    # 3. Tornar NOT NULL
    op.alter_column('books', 'status', nullable=False)

def downgrade():
    op.drop_column('books', 'status')
```

## 🐳 Docker Compose + Migrações

### **Opção 1: Manual (recomendado para dev)**
```bash
docker-compose exec web flask db upgrade
```

### **Opção 2: Automático no startup**

Adicionar em `docker-compose.yml`:
```yaml
services:
  web:
    # ...
    command: >
      sh -c "flask db upgrade && python run.py"
```

### **Opção 3: Script de entrypoint**

Criar `docker-entrypoint.sh`:
```bash
#!/bin/bash
flask db upgrade
exec "$@"
```

## 🎯 Exemplo Completo

```bash
# 1. Modificar modelo
# app/models.py: adicionar campo 'publisher'

# 2. Gerar migração
docker-compose exec web flask db migrate -m "adicionar campo publisher"

# 3. Revisar arquivo gerado
cat migrations/versions/*_adicionar_campo_publisher.py

# 4. Aplicar
docker-compose exec web flask db upgrade

# 5. Verificar
docker-compose exec web flask db current

# 6. Se algo der errado, reverter
docker-compose exec web flask db downgrade
```

## 📝 Troubleshooting

### **Erro: "Can't locate revision identified by..."**
```bash
# Resetar completamente (cuidado: perde dados!)
docker-compose down -v
docker-compose up -d
docker-compose exec web flask db upgrade
```

### **Erro: "Target database is not up to date"**
```bash
flask db stamp head  # Marca todas como aplicadas
```

### **Migrações conflitantes (merge de branches)**
```bash
flask db merge heads -m "merge de branches"
```

## 🔗 Referências

- [Flask-Migrate Docs](https://flask-migrate.readthedocs.io/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
