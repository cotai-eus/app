from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, bids, calendar, config, contacts, documents, 
    messages, users, api_keys, profile, sessions
)

# Cria o router principal para a API v1
# Creates the main router for API v1
api_router = APIRouter()

# Adiciona todos os routers específicos de recursos
# Adds all resource-specific routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bids.router, prefix="/bids", tags=["bids"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
