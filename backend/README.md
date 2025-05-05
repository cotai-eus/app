# Licitação Hub API

Uma API robusta e assíncrona para gerenciamento de licitações, análise de documentos e comunicação.

## Visão Geral do Projeto

O Licitação Hub API é um backend construído em Python com FastAPI, projetado para suportar um sistema completo de gerenciamento de licitações. O sistema permite o upload e análise de documentos de licitação usando modelos de linguagem (LLM), gerenciamento de status de licitações, comunicação entre usuários e agendamento de eventos.

## Tecnologias

*   **Framework:** FastAPI
*   **Linguagem:** Python 3.12
*   **Banco de Dados:** PostgreSQL 16
*   **ORM:** SQLAlchemy 2.0 (com asyncio)
*   **Migrações:** Alembic
*   **Validação:** Pydantic v2
*   **Autenticação:** JWT (python-jose, passlib)
*   **Cache/Queue:** Redis
*   **Cliente HTTP Async:** HTTPX
*   **Logging:** Structlog
*   **Containerização:** Docker, Docker Compose
*   **Gerenciador de Dependências:** Poetry

## Estrutura do Projeto

```
/backend
├── alembic/          # Configuração e scripts de migração Alembic
├── app/              # Código fonte da aplicação FastAPI
│ ├── api/            # Módulos da API (endpoints, dependências)
│ ├── core/           # Configuração central, segurança
│ ├── crud/           # Operações de banco de dados (Create, Read, Update, Delete)
│ ├── db/             # Configuração da sessão do banco, modelo base
│ ├── models/         # Modelos SQLAlchemy (definição das tabelas)
│ ├── schemas/        # Schemas Pydantic (validação de dados)
│ ├── services/       # Lógica de negócios, serviços externos (LLM)
│ ├── tasks/          # Tarefas assíncronas (processamento de documentos)
│ └── main.py         # Ponto de entrada da aplicação FastAPI
├── tests/            # Testes automatizados (pytest)
├── .env.example      # Exemplo de arquivo de variáveis de ambiente
├── .gitignore        # Arquivos ignorados pelo Git
├── alembic.ini       # Configuração do Alembic
├── Dockerfile        # Instruções para construir a imagem Docker do backend
├── docker-compose.yml # Orquestração dos containers (backend, db, redis)
├── pyproject.toml    # Definição do projeto e dependências (Poetry)
└── README.md         # Este arquivo
```

## Configuração

1.  **Instalar Docker e Docker Compose:** Certifique-se de que ambos estão instalados em seu sistema.
2.  **Copiar Arquivo de Ambiente:**
    ```bash
    cp .env.example .env
    ```
3.  **Editar `.env`:** Abra o arquivo `.env` e configure as variáveis necessárias:
    *   `SECRET_KEY`: Gere uma chave segura (e.g., `openssl rand -hex 32`).
    *   `POSTGRES_PASSWORD`: Defina uma senha segura para o banco de dados.
    *   `LLM_API_KEY`: Insira sua chave de API para o provedor LLM configurado (`LLM_PROVIDER`).
    *   `FIRST_SUPERUSER_EMAIL` / `FIRST_SUPERUSER_PASSWORD`: Credenciais para o usuário administrador inicial (será criado na primeira inicialização se `init_db` for usado, ou pode ser criado manualmente/via script).
    *   Ajuste outras variáveis como `BACKEND_CORS_ORIGINS` conforme necessário.

## Execução (Docker Compose)

1.  **Construir e Iniciar os Containers:**
    No diretório `c:\Users\user\Desktop\app\backend`, execute:
    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: Reconstrói as imagens se houver alterações no `Dockerfile` ou código fonte.
    *   `-d`: Executa os containers em segundo plano (detached mode).

2.  **Aplicar Migrações do Banco de Dados:**
    Após os containers estarem rodando, execute as migrações do Alembic dentro do container do backend:
    ```bash
    docker-compose exec backend alembic upgrade head
    ```
    *Nota: Na primeira vez, isso criará todas as tabelas, extensões e triggers definidos na migração inicial.*

3.  **Acessar a API:**
    A API estará disponível em `http://localhost:8000` (ou a porta mapeada no `docker-compose.yml`).
    *   **Documentação Interativa (Swagger):** `http://localhost:8000/docs`
    *   **Documentação Alternativa (ReDoc):** `http://localhost:8000/redoc`

4.  **Parar os Containers:**
    ```bash
    docker-compose down
    ```
    *   Para remover os volumes (dados do banco e Redis), use `docker-compose down -v`.

## Desenvolvimento Local (Sem Docker, Opcional)

1.  **Instalar Python 3.12+ e Poetry.**
2.  **Instalar Dependências:**
    ```bash
    poetry install
    ```
3.  **Configurar Banco de Dados e Redis:** Certifique-se de ter instâncias do PostgreSQL e Redis rodando localmente e atualize as URLs (`DATABASE_URL`, `REDIS_URL`) no arquivo `.env`.
4.  **Aplicar Migrações:**
    ```bash
    poetry run alembic upgrade head
    ```
5.  **Executar o Servidor Uvicorn:**
    ```bash
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

## Testes

1.  **Configurar Banco de Dados de Teste:** Certifique-se de que a URL `TEST_DATABASE_URL` em `tests/conftest.py` aponta para um banco de dados de teste (ele será modificado pelos testes). Pode ser o mesmo servidor, mas um banco diferente (e.g., `appdb_test`). Crie este banco manualmente se necessário.
2.  **Executar Testes com Pytest:**
    Dentro do ambiente Poetry (ou via `docker-compose exec backend`):
    ```bash
    poetry run pytest tests/
    ```
    Para incluir cobertura de código:
    ```bash
    poetry run pytest --cov=app --cov-report=term-missing tests/
    ```

## Linting e Formatação

Ferramentas configuradas no `pyproject.toml` (Black, Ruff, isort, Mypy). Use com `pre-commit` ou execute manualmente:

```bash
poetry run black .
poetry run ruff check . --fix
poetry run isort .
poetry run mypy app/
```

## Próximos Passos / Considerações

*   **Criação do Superusuário:** Implementar um script (`app/db/init_db.py` ou um comando Typer/Click) para criar o superusuário inicial de forma idempotente.
*   **Validação Detalhada:** Aprimorar a validação das `answers` em `FormResponse` contra a `structure` do `Form`.
*   **Tratamento de Arquivos:** Para uploads de PDF maiores, implementar armazenamento em nuvem (S3, Azure Blob Storage) em vez de processar em memória. Salvar referência ao arquivo no banco (e.g., em `FormResponse.source_pdf_id` ou tabela `Documents`).
*   **Filas de Tarefas Robustas:** Para alta carga, substituir `BackgroundTasks` do FastAPI por Celery com Redis/RabbitMQ para maior robustez e escalabilidade no processamento de documentos.
*   **WebSockets:** Implementar WebSockets para notificações em tempo real (novas mensagens, status de processamento de documentos).
*   **Rate Limiting:** Adicionar rate limiting aos endpoints da API (e.g., usando `slowapi`).
*   **Segurança:** Revisar configurações de CORS, Trusted Hosts, e considerar headers de segurança adicionais. Implementar refresh tokens.
*   **Testes:** Expandir a cobertura de testes, incluindo testes de integração e testes para a lógica de serviços (LLM, processamento).
*   **Monitoramento e Logging:** Configurar `structlog.processors.JSONRenderer()` para produção e integrar com sistemas de monitoramento (Prometheus, Grafana, ELK/EFK stack).
# cotai-dev
