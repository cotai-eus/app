# Facilita a importação dos objetos CRUD
from .crud_user import user
from .crud_contact import contact
from .crud_message import message
from .crud_calendar_event import calendar_event
from .crud_form import form
from .crud_form_response import form_response

# Adicionar outros CRUDS aqui se necessário (e.g., crud_user_photo)

__all__ = [
    "user",
    "contact",
    "message",
    "calendar_event",
    "form",
    "form_response",
]
