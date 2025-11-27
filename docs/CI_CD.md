# 🔄 Integração Contínua (CI/CD)

## 📋 Visão Geral

Este projeto usa **GitHub Actions** para executar automaticamente:
- ✅ Testes unitários
- 🔍 Análise de código
- 🔒 Verificações de segurança
- 🐳 Build da imagem Docker

## 🚀 Workflows Configurados

### **CI - Testes e Validação** (`.github/workflows/ci.yml`)

Executado em:
- Push para `main` ou `develop`
- Pull Requests para `main` ou `develop`

#### Jobs:

1. **test** - Testes Python
   - Roda testes com pytest
   - Gera relatório de cobertura
   - Usa PostgreSQL como serviço
   - Matrix strategy: Python 3.11

2. **lint** - Análise de Código
   - mypy: verificação de tipos
   - safety: vulnerabilidades em dependências
   - bandit: análise de segurança
   - flake8/black: formatação

3. **docker** - Build Docker
   - Verifica se imagem pode ser construída
   - Valida Dockerfile

## 📊 Status Badges

Adicione ao README.md:

```markdown
![CI Status](https://github.com/arthurliszkievich/flask-books-api/workflows/CI%20-%20Testes%20e%20Validação/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

## 🔧 Executar Localmente

### Testes
```bash
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Formatação
```bash
pip install black
black app/ tests/
```

### Lint
```bash
pip install flake8
flake8 app/ tests/ --max-line-length=127
```

### Análise de Segurança
```bash
pip install bandit safety
bandit -r app/
safety check
```

## 🎯 Boas Práticas

1. **Sempre rode os testes localmente** antes de fazer push
2. **Corrija warnings** de lint antes de criar PR
3. **Mantenha cobertura acima de 80%**
4. **Nunca desabilite checks de segurança**

## 🔐 Segredos no GitHub

Para deploy automático, configure:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `DEPLOY_KEY` (se aplicável)

**Settings → Secrets and variables → Actions → New repository secret**

## 📈 Melhorias Futuras

- [ ] Deploy automático para staging
- [ ] Testes de integração E2E
- [ ] Performance benchmarks
- [ ] Análise de segurança SAST/DAST
- [ ] Build e push de imagem Docker para registry
