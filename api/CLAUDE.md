# API - SGAA

## Convenções

- Nomes de variáveis, funções e campos de tabelas do banco em português.
- Tabelas têm campos de auditoria: `criado_em`, `atualizado_em`, `deletado_em` (soft delete).

## Regras de trabalho

Comandos executados dentro de `api/`.

1. Antes de executar uma tarefa, rodar os linters e os testes automatizados, e rodar de novo ao concluir:
   - `poetry run ruff check .`
   - `poetry run ruff format --check .`
   - `poetry run pytest`
2. Executar as migrations (`poetry run alembic upgrade head`) antes dos testes e sempre que criar ou alterar uma migração. Ao criar uma, validar também o caminho de volta (`poetry run alembic downgrade -1` e `upgrade head` de novo).

Os testes e as migrations precisam de um PostgreSQL acessível pela `DATABASE_URL`. Se não houver um disponível, subir um local com Docker:

```bash
docker run -d --name sgaa-test -p 5432:5432 \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=sgaa_test \
  postgres:15
export DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/sgaa_test
```

Se não for possível rodar os testes ou as migrations, dizer isso explicitamente no resumo da tarefa em vez de apresentá-la como verificada.

## Contexto

- A API serve uma versão web e uma versão mobile (Android).
- A versão web e a API são deployadas na Vercel (serverless).
