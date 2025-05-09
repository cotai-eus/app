
# 📄 Relatório Completo: **Licitação Hub API**

---

## 🔍 1. Visão Geral

O **Licitação Hub** é uma API robusta e assíncrona desenvolvida com **FastAPI** para:

- Gerenciamento de licitações
- Análise inteligente de documentos PDF
- Comunicação entre usuários

A arquitetura é modular e moderna, utilizando:

- **SQLAlchemy 2.0** com PostgreSQL (modo assíncrono)
- Autenticação via **JWT**
- Redis para cache e filas
- Processamento assíncrono com **BackgroundTasks**
- Infraestrutura com **Docker Compose**

---

## 🧱 2. Estrutura do Projeto

```bash
/backend
├── alembic/          # Migrações de banco de dados
├── app/
│   ├── api/          # Endpoints da API
│   │   ├── endpoints/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/         # Configurações e segurança
│   ├── crud/         # Operações CRUD
│   ├── db/           # Banco de dados
│   ├── models/       # Modelos SQLAlchemy
│   ├── schemas/      # Schemas Pydantic
│   ├── services/     # Lógicas de negócio
│   ├── tasks/        # Tarefas assíncronas
│   ├── redis/        # Cliente Redis
│   └── main.py       # Ponto de entrada da aplicação
```

---

## 🔌 3. Endpoints Principais

### 📁 API v1 (`/api/v1/`)

#### 🔐 Autenticação (`/auth`)
- `POST /token`: Login com JWT
- `POST /signup`: Registro
- `POST /login`: Login com "lembrar de mim"

#### 👤 Usuários (`/users`)
- `GET /me`, `PUT /me`
- `GET /`, `GET /{user_id}`, `PUT /{user_id}` (admin)

#### 📄 Documentos (`/documents`)
- `POST /upload`, `GET /`, `GET /{id}`

#### 💬 Mensagens (`/messages`)
- `GET /`, `POST /`

#### 📇 Contatos (`/contacts`)
- `GET /`, `POST /`

#### 📆 Calendário (`/calendar`)
- Gestão de eventos

#### ⚙️ Configuração (`/config`)
- `GET /api-keys`, `POST /api-keys`

#### 📦 Licitações (`/bids`)
- Gestão de licitações

### 🚀 API Direta

#### 📝 Formulários (`/forms`)
- `POST/GET /templates`, `PUT/DELETE /templates/{id}`
- `POST /responses`, `GET /responses`

#### 🧠 Processamento de PDF
- `POST /documents/process`

---

## 🚀 4. Redis

Utilizado para **cache** e **filas assíncronas**, com funções:

```python
get_redis_client()
close_redis_connection()
set_key(), get_key(), delete_key()
get_json()
add_to_cache_set(), is_in_cache_set()
```

---

## 🔄 5. CRUD

Padrão genérico implementado via `CRUDBase`:

- `get()`, `get_multi()`, `create()`, `update()`, `remove()`

### Especializações:
- `user`, `form`, `form_response`, `message`, `contact`, `calendar_event`

---

## ⚙️ 6. Core

Componentes centrais:

- `config.py`: Variáveis de ambiente (Pydantic)
- `security.py`: JWT, hashing
- `logging.py`: Logs estruturados
- `cli.py`: Comandos de terminal

---

## 🗃️ 7. DB

Módulo de banco com:

- `session.py`: Sessão assíncrona
- `base_class.py`: Classe base com:
  - UUID como PK
  - `created_at`, `updated_at`
- `base.py`: Suporte ao Alembic

---

## 🧩 8. Models

Modelos de dados:

- `User`, `Contact`, `Message`, `CalendarEvent`
- `Form`, `FormResponse`, `Document`
- `ApiKey`, `ActiveSession`

---

## 🧪 9. Schemas

Validação com **Pydantic**:

- Usuários: `UserBase`, `UserCreate`, `UserPublic`
- Autenticação: `Token`, `TokenPayload`
- Formulários: `Form`, `FormCreate`
- Respostas: `FormResponse`, `FormResponseCreate`
- Documentos: `DocumentPublic`, `DocumentCreate`
- API Keys: `ApiKeyPublic`, `ApiKeyCreate`

---

## 🧠 10. Services

Serviços especializados:

- `llm_service.py`: Processamento de linguagem natural para extração de dados de PDFs

---

## 🔁 11. Tasks

Tarefas assíncronas com `BackgroundTasks`:

- `process_document_task()`
- `process_uploaded_bid_document()`

---

## 🐳 12. Acesso via Docker Compose

### 📦 Serviços:

| Serviço    | Porta | Função                              |
|------------|-------|-------------------------------------|
| frontend   | 8080  | Interface web via Nginx             |
| backend    | 9000  | API FastAPI principal               |
| db         | 5432  | PostgreSQL 16                       |
| redis      | 6379  | Cache e filas                       |
| pgadmin    | 5050  | Admin. do banco                     |

### ▶️ Como iniciar:

```bash
# Subir contêineres
docker-compose up --build -d

# Aplicar migrações Alembic
docker-compose exec backend alembic upgrade head
```

### 🔗 Acesso rápido:

- **API**: [http://localhost:9000](http://localhost:9000)
- **Swagger**: [http://localhost:9000/docs](http://localhost:9000/docs)
- **ReDoc**: [http://localhost:9000/redoc](http://localhost:9000/redoc)
- **Frontend**: [http://localhost:8080](http://localhost:8080)
- **PgAdmin**: [http://localhost:5050](http://localhost:5050)

---

> ✅ A arquitetura completa do **Licitação Hub API** combina escalabilidade, segurança e performance, oferecendo uma solução de ponta para o gerenciamento inteligente de processos licitatórios.