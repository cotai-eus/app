# Agrupa todos os routers da API
from fastapi import APIRouter

# Use relative imports for endpoint modules
from . import auth
from . import users
# Add other endpoint modules similarly if they exist and have routers
# from . import bids
# from . import calendar
# from . import config
# from . import contacts
# from . import documents
# from . import messages

api_router = APIRouter()

# Inclui os routers de cada módulo, definindo prefixos e tags para organização na documentação Swagger
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# Include other routers as needed
# api_router.include_router(bids.router, prefix="/bids", tags=["bids"])
# api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
# api_router.include_router(config.router, prefix="/config", tags=["config"])
# api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
# api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
# api_router.include_router(messages.router, prefix="/messages", tags=["messages"])

