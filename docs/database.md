# Documentação do Banco de Dados - Licitação Hub

## Visão Geral

O Licitação Hub utiliza PostgreSQL como sistema de gerenciamento de banco de dados relacional. Esta documentação fornece informações sobre a configuração do banco de dados, estrutura e administração.

## Configuração de Conexão

### Configurações Padrão
- **Usuário**: postgres
- **Senha**: postgres
- **Host**: 
  - `localhost` (quando executado localmente)
  - `db` (quando executado dentro do Docker)
- **Porta**: 5432
- **Nome do Banco**: licitacao_hub
- **URL de Conexão**: `postgresql+psycopg://postgres:postgres@db:5432/licitacao_hub`

### Variáveis de Ambiente

As configurações do banco de dados são definidas através das seguintes variáveis de ambiente no arquivo `.env`:

