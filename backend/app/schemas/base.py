import uuid
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    """
    Classe base para todos os schemas Pydantic.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
    )

class IdMixin(BaseSchema):
    """
    Mixin para schemas que incluem ID.
    """
    id: uuid.UUID

class TimestampMixin(BaseSchema):
    """
    Mixin para schemas que incluem timestamps.
    """
    created_at: datetime
    updated_at: datetime