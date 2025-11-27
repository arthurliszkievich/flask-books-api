# Script PowerShell para inicializar o projeto pela primeira vez

Write-Host "🚀 Inicializando Flask Books API..." -ForegroundColor Cyan

# 1. Verificar se Docker está rodando
Write-Host "📦 Verificando Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
}
catch {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker Desktop." -ForegroundColor Red
    exit 1
}

# 2. Parar containers existentes
Write-Host "🛑 Parando containers existentes..." -ForegroundColor Yellow
docker-compose down

# 3. Rebuild da imagem
Write-Host "🔨 Reconstruindo imagem Docker..." -ForegroundColor Yellow
docker-compose build --no-cache web

# 4. Subir containers
Write-Host "⬆️ Subindo containers..." -ForegroundColor Yellow
docker-compose up -d

# 5. Aguardar banco estar pronto
Write-Host "⏳ Aguardando banco de dados..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 6. Inicializar Flask-Migrate
Write-Host "🗄️ Inicializando migrações..." -ForegroundColor Yellow
docker-compose exec -T web flask db init 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ℹ️ Migrations já inicializadas" -ForegroundColor Gray
}

# 7. Gerar migração inicial
Write-Host "📝 Gerando migração inicial..." -ForegroundColor Yellow
docker-compose exec -T web flask db migrate -m "Criar tabela books inicial"

# 8. Aplicar migração
Write-Host "✅ Aplicando migração..." -ForegroundColor Yellow
docker-compose exec -T web flask db upgrade

# 9. Verificar status
Write-Host "🔍 Verificando status..." -ForegroundColor Yellow
docker-compose exec -T web flask db current

Write-Host ""
Write-Host "✅ Inicialização completa!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Acesse a API em: http://localhost:5000/api/books" -ForegroundColor Cyan
Write-Host "❤️ Health check: http://localhost:5000/api/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Ver logs: docker-compose logs -f web" -ForegroundColor Gray
Write-Host "🛑 Parar: docker-compose down" -ForegroundColor Gray
