#!/bin/bash
# Script para inicializar o projeto pela primeira vez

echo "🚀 Inicializando Flask Books API..."

# 1. Verificar se Docker está rodando
echo "📦 Verificando Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

# 2. Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# 3. Rebuild da imagem
echo "🔨 Reconstruindo imagem Docker..."
docker-compose build --no-cache web

# 4. Subir containers
echo "⬆️ Subindo containers..."
docker-compose up -d

# 5. Aguardar banco estar pronto
echo "⏳ Aguardando banco de dados..."
sleep 5

# 6. Inicializar Flask-Migrate
echo "🗄️ Inicializando migrações..."
docker-compose exec -T web flask db init || echo "Migrations já inicializadas"

# 7. Gerar migração inicial
echo "📝 Gerando migração inicial..."
docker-compose exec -T web flask db migrate -m "Criar tabela books inicial"

# 8. Aplicar migração
echo "✅ Aplicando migração..."
docker-compose exec -T web flask db upgrade

# 9. Verificar status
echo "🔍 Verificando status..."
docker-compose exec -T web flask db current

echo ""
echo "✅ Inicialização completa!"
echo ""
echo "📚 Acesse a API em: http://localhost:5000/api/books"
echo "❤️ Health check: http://localhost:5000/api/health"
echo ""
echo "📊 Ver logs: docker-compose logs -f web"
echo "🛑 Parar: docker-compose down"
