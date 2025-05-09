-- Extensão para UUID, se não estiver habilitada
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Extensão para CITEXT (case-insensitive text), se não estiver habilitada
CREATE EXTENSION IF NOT EXISTS "citext";

-- Tabela de Usuários
CREATE TABLE "user" (
    "user_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "username" CITEXT UNIQUE NOT NULL,
    "email" CITEXT UNIQUE NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL,
    "full_name" VARCHAR(255) NOT NULL,
    "avatar_url" TEXT, -- Armazena o caminho/URL para o avatar
    "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
    "is_admin" BOOLEAN NOT NULL DEFAULT FALSE,
    "last_login" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_user_email" ON "user" ("email");
CREATE INDEX IF NOT EXISTS "idx_user_username" ON "user" ("username");

-- Tabela de Configurações do Usuário
CREATE TABLE "user_config" (
    "config_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "user_id" UUID UNIQUE NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE,
    "theme" VARCHAR(50) NOT NULL DEFAULT 'system', -- e.g., 'light', 'dark', 'system'
    "ui_density" VARCHAR(50) NOT NULL DEFAULT 'normal', -- e.g., 'compact', 'normal', 'comfortable'
    "notifications" JSONB, -- Armazena preferências de notificação como JSON
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_user_config_user_id" ON "user_config" ("user_id");

-- Tabela de Sessões Ativas
CREATE TABLE "active_session" (
    "session_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE,
    "device_info" VARCHAR(255),
    "ip_address" VARCHAR(45), -- Suporta IPv6
    "last_accessed_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "is_revoked" BOOLEAN NOT NULL DEFAULT FALSE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_active_session_user_id" ON "active_session" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_active_session_last_accessed_at" ON "active_session" ("last_accessed_at");

-- Tabela de Chaves de API
CREATE TABLE "api_key" (
    "key_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE,
    "name" VARCHAR(255) NOT NULL,
    "prefix" VARCHAR(8) NOT NULL UNIQUE, -- Prefixo da chave para identificação
    "hashed_key" VARCHAR(255) NOT NULL UNIQUE, -- Hash da chave real
    "permissions" TEXT[], -- Array de strings para permissões
    "last_used" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_api_key_user_id" ON "api_key" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_api_key_prefix" ON "api_key" ("prefix");

-- Define enumerated types for event categories and priorities
CREATE TYPE event_type AS ENUM ('prazo', 'reuniao', 'licitacao', 'outro');
CREATE TYPE event_priority AS ENUM ('baixa', 'media', 'alta');

-- Tabela de Eventos do Calendário
CREATE TABLE "calendar_event" (
    "event_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "date" TIMESTAMPTZ NOT NULL,
    "start_time" TIME,
    "end_time" TIME,
    "type" event_type NOT NULL,
    "priority" event_priority NOT NULL DEFAULT 'media',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE "calendar_event" IS 'Stores all calendar events with deadlines and meetings';
COMMENT ON COLUMN "calendar_event"."type" IS 'Event category: deadline, meeting, bid, or other';

-- Add index for bid relationship
CREATE INDEX IF NOT EXISTS "idx_calendar_event_user_id" ON "calendar_event" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_calendar_event_date" ON "calendar_event" ("date");
CREATE INDEX IF NOT EXISTS "idx_calendar_event_type" ON "calendar_event" ("type");
CREATE INDEX IF NOT EXISTS "idx_calendar_event_related_bid" ON "calendar_event" ("related_bid_id");

-- Tabela de Documentos (Editais, etc.)
-- Armazena metadados dos arquivos. Os arquivos em si são guardados no sistema de arquivos ou object storage.
CREATE TABLE "document" (
    "document_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "uploaded_by_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE RESTRICT,
    "related_bid_id" UUID REFERENCES "bid"("bid_id") ON DELETE SET NULL, -- Se o documento está diretamente ligado a uma licitação
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "file_name" VARCHAR(255) NOT NULL, -- Nome original do arquivo
    "file_path" TEXT NOT NULL UNIQUE, -- Caminho no sistema de arquivos ou URL no object storage
    "file_size" BIGINT NOT NULL, -- Tamanho em bytes
    "mime_type" VARCHAR(100) NOT NULL,
    "platform" VARCHAR(100), -- Plataforma de origem (e.g., 'ComprasNet', 'BEC', 'Manual')
    "document_type" VARCHAR(100) NOT NULL, -- e.g., 'edital', 'anexo', 'proposta', 'contrato'
    "document_number" VARCHAR(100),
    "entity" VARCHAR(255), -- Órgão emissor
    "processing_status" VARCHAR(20) NOT NULL DEFAULT 'pending', -- e.g., 'pending', 'processing', 'completed', 'error'
    "processed_at" TIMESTAMPTZ,
    "extracted_text" TEXT, -- Texto extraído do documento (OCR)
    "llm_analysis" JSONB, -- Resultados da análise por IA
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_document_uploaded_by_id" ON "document" ("uploaded_by_id");
CREATE INDEX IF NOT EXISTS "idx_document_related_bid_id" ON "document" ("related_bid_id");
CREATE INDEX IF NOT EXISTS "idx_document_title" ON "document" ("title");
CREATE INDEX IF NOT EXISTS "idx_document_platform" ON "document" ("platform");
CREATE INDEX IF NOT EXISTS "idx_document_type" ON "document" ("document_type");

-- Tabela de Licitações
CREATE TABLE "bid" (
    "bid_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE, -- Usuário que cadastrou/gerencia
    "source_document_id" UUID REFERENCES "document"("document_id") ON DELETE SET NULL, -- Edital principal
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "number" VARCHAR(100), -- Número da licitação/processo
    "organization" VARCHAR(255), -- Órgão licitante
    "publication_date" TIMESTAMPTZ,
    "deadline_date" TIMESTAMPTZ,
    "status" VARCHAR(50) NOT NULL DEFAULT 'recebidos',
    -- Status para Kanban: 'recebidos', 'analisados', 'enviados', 'respondidos', 'ganho', 'perdido', 'arquivado'
    "status_changed_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "analysis_result" JSONB, -- Resultado da análise da IA sobre a licitação
    "value" DECIMAL(15, 2), -- Valor estimado ou proposto
    "modality" VARCHAR(100), -- Modalidade (e.g., 'Pregão Eletrônico', 'Concorrência')
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_bid_user_id" ON "bid" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_bid_status" ON "bid" ("status");
CREATE INDEX IF NOT EXISTS "idx_bid_deadline_date" ON "bid" ("deadline_date");
CREATE INDEX IF NOT EXISTS "idx_bid_title" ON "bid" ("title");

-- Tabela de Associação Documento-Licitação (Muitos-para-Muitos, se necessário para outros documentos além do edital principal)
-- Se um documento pode estar em várias licitações e uma licitação ter vários documentos (além do edital principal)
CREATE TABLE "bid_document_association" (
    "bid_id" UUID NOT NULL REFERENCES "bid"("bid_id") ON DELETE CASCADE,
    "document_id" UUID NOT NULL REFERENCES "document"("document_id") ON DELETE CASCADE,
    "document_role" VARCHAR(50), -- e.g., 'anexo_tecnico', 'proposta_comercial', 'esclarecimento'
    PRIMARY KEY ("bid_id", "document_id", "document_role") -- Role para permitir o mesmo doc com papéis diferentes
);

CREATE INDEX IF NOT EXISTS "idx_bid_document_association_bid_id" ON "bid_document_association" ("bid_id");
CREATE INDEX IF NOT EXISTS "idx_bid_document_association_document_id" ON "bid_document_association" ("document_id");

-- Tabela de Mensagens (para chat ou notificações internas)
CREATE TABLE "message" (
    "message_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "sender_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE,
    "recipient_id" UUID REFERENCES "user"("user_id") ON DELETE CASCADE, -- Pode ser NULL para mensagens de sistema ou em grupo
    "bid_id" UUID REFERENCES "bid"("bid_id") ON DELETE SET NULL, -- Mensagem relacionada a uma licitação específica
    "channel" VARCHAR(100), -- e.g., 'licitacao_XYZ', 'geral', 'direct_user1_user2'
    "content" TEXT NOT NULL,
    "is_read" BOOLEAN NOT NULL DEFAULT FALSE,
    "sent_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_message_sender_id" ON "message" ("sender_id");
CREATE INDEX IF NOT EXISTS "idx_message_recipient_id" ON "message" ("recipient_id");
CREATE INDEX IF NOT EXISTS "idx_message_bid_id" ON "message" ("bid_id");
CREATE INDEX IF NOT EXISTS "idx_message_channel" ON "message" ("channel");
CREATE INDEX IF NOT EXISTS "idx_message_sent_at" ON "message" ("sent_at");

-- Tabela de Contatos (se houver um sistema de contatos/CRM)
CREATE TABLE "contact" (
    "contact_id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL REFERENCES "user"("user_id") ON DELETE CASCADE, -- Usuário que 'possui' este contato
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255),
    "phone" VARCHAR(50),
    "organization" VARCHAR(255),
    "role" VARCHAR(100),
    "notes" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS "idx_contact_user_id" ON "contact" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_contact_name" ON "contact" ("name");
CREATE INDEX IF NOT EXISTS "idx_contact_email" ON "contact" ("email");

-- Funções para atualizar automaticamente o campo 'updated_at'
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar o trigger a todas as tabelas que possuem 'updated_at'
DO $$
DECLARE
    t_name TEXT;
BEGIN
    FOR t_name IN (SELECT table_name FROM information_schema.columns WHERE column_name = 'updated_at')
    LOOP
        EXECUTE format('CREATE TRIGGER set_timestamp
                        BEFORE UPDATE ON %I
                        FOR EACH ROW
                        EXECUTE PROCEDURE trigger_set_timestamp();', t_name);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
