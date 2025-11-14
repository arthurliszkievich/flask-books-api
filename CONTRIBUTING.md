# Contribuindo para o Flask Books API

Obrigado por contribuir! Siga estas orientações para facilitar revisões.

Fluxo de trabalho
1. Fork do repositório
2. Criar branch com nome descritivo:
   git checkout -b feat/auth-jwt
3. Implementar mudanças e escrever testes
4. Commit claro:
   git commit -m "feat: adicionar login JWT"
5. Push e abrir Pull Request

Padrões de código
- Siga PEP8 (use black e isort se possível)
- Mensagens de commit em inglês são preferíveis para portfólios públicos

Testes
- Adicione/atualize testes para novas features
- `pytest` como runner

Revisões e PR
- Descreva o propósito da PR
- Inclua passos para testar manualmente (se aplicável)
- Linke issues correspondentes

Segurança
- Não inclua segredos no repo (use .env e variáveis de ambiente)