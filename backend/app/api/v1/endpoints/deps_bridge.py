"""
Bridge module that re-exports dependency functions from app.api.deps.
This allows endpoints to import dependencies from a common location
while maintaining the ability to swap implementations if needed.
"""

from app.api.deps import (
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    get_current_active_admin,
    get_db,
    get_api_key_user
)

# Re-export all dependencies
__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "get_current_active_admin",
    "get_db",
    "get_api_key_user"
]
