# Permite importar schemas diretamente do pacote app.schemas

from app.schemas.api_key import (
    ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyInDB, ApiKeyPublic,
)
from app.schemas.bid import (
    BidBase, BidCreate, BidInDB, BidPublic, BidSignRequest, BidStatusUpdate, BidUpdate,
)
from app.schemas.calendar import (
    CalendarEventBase, CalendarEventCreate, CalendarEventInDB,
    CalendarEventPublic, CalendarEventUpdate,
)
from app.schemas.contact import (
    ContactBase, ContactCreate, ContactInDB, ContactPublic, ContactUpdate,
    ContactWithRecentMessage,
)
from app.schemas.document import (
    DocumentBase, DocumentCreate, DocumentInDB, DocumentPublic,
    DocumentUpdate, DocumentWithAnalysis,
)
from app.schemas.message import (
    MessageBase, MessageCreate, MessageInDB, MessagePublic, MessageUpdate,
)
from app.schemas.session import (
    ActiveSessionBase, ActiveSessionCreate, ActiveSessionInDB, ActiveSessionPublic,
)
from app.schemas.token import LoginRequest, Token, TokenPayload
from app.schemas.user import (
    UserBase, UserCreate, UserCreateDB, UserInDB, UserPublic,
    UserUpdate, UserUpdateDB, UserWithPassword,
)
from .contact import Contact, ContactCreate, ContactUpdate
from .message import Message, MessageCreate
from .calendar_event import CalendarEvent, CalendarEventCreate, CalendarEventUpdate
from .form import Form, FormCreate, FormUpdate
from .form_response import FormResponse, FormResponseCreate, FormResponseUpdate, FormResponseStatus
from .msg import Msg

# __all__ define quais nomes são exportados quando se faz 'from app.schemas import *'
# É uma boa prática definir, embora não seja estritamente necessário aqui.
__all__ = [
    "Token",
    "TokenPayload",
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UserUpdateMe",
    "Contact",
    "ContactCreate",
    "ContactUpdate",
    "Message",
    "MessageCreate",
    "CalendarEvent",
    "CalendarEventCreate",
    "CalendarEventUpdate",
    "Form",
    "FormCreate",
    "FormUpdate",
    "FormResponse",
    "FormResponseCreate",
    "FormResponseUpdate",
    "FormResponseStatus",
    "Msg",
]
