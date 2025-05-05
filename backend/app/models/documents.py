import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class UserPhoto(Base):
    """
    Modelo para fotos dos usuários.
    """
    __tablename__ = "user_photos"
    
    # Substituindo o ID padrão pelo específico user_photos.photo_id
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        name="photo_id"
    )
    
    # Chave estrangeira para usuário
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # URL da foto (ex: em armazenamento em nuvem)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    
    # Descrição opcional
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relacionamentos
    user: Mapped["User"] = relationship(back_populates="photos")

# (Criar este arquivo se for necessário armazenar metadados de PDFs)
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMPTZ

if TYPE_CHECKING:
    from .users import User  # noqa: F401
    from .form_responses import FormResponse # noqa F401

class Document(Base):
    """
    Modelo SQLAlchemy para metadados de Documentos (ex: PDFs processados).
    """
    __tablename__ = "documents" # Nome da tabela referenciada em FormResponse

    document_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True) # Usuário que fez upload
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String)
    storage_url: Mapped[Optional[str]] = mapped_column(Text) # URL no S3, GCS, etc.
    file_size: Mapped[Optional[int]] = mapped_column() # Em bytes
    # Adicionar outros metadados relevantes, ex: hash do arquivo
    uploaded_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ(timezone=True), server_default=func.timezone('utc', func.now())
    )
    # Status do processamento do documento em si, se houver
    processing_status: Mapped[Optional[str]] = mapped_column(Text, index=True) # Ex: uploaded, processing, processed, error

    # Relacionamentos
    uploader: Mapped[Optional["User"]] = relationship()
    # Relacionamento com form_responses que usaram este documento como fonte
    form_responses: Mapped[List["FormResponse"]] = relationship() # Configurar back_populates se necessário