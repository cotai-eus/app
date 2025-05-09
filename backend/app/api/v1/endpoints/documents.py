import os
import uuid
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentPublic, DocumentUpdate
from app.tasks.processing import process_uploaded_bid_document

router = APIRouter()
logger = structlog.get_logger()

@router.post("", response_model=DocumentPublic, status_code=status.HTTP_201_CREATED)
async def create_document(
    *,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    platform: str = Form(...),
    type: str = Form(...),
    number: str = Form(...),
    entity: str = Form(...),
    description: Optional[str] = Form(None),
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Criar um novo documento/edital
    # Create a new document/bid notice
    """
    # Verificar tipo do arquivo
    if not file.content_type in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de arquivo não suportado. Apenas PDF, DOC, DOCX, XLS e XLSX são permitidos."
        )
    
    # Gerar nome único para o arquivo
    file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ""
    filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Preparar diretório de upload
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
    
    # Salvar arquivo
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Criar registro do documento no banco
    document_data = {
        "title": f"{type} - {number} - {entity}",
        "description": description,
        "file_name": file.filename,
        "file_path": file_path,
        "file_size": len(contents),
        "mime_type": file.content_type,
        "platform": platform,
        "document_type": type,
        "document_number": number,
        "entity": entity,
        "uploaded_by_id": current_user.user_id,
        "processing_status": "pending"
    }
    
    document = Document(**document_data)
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    # Iniciar processamento assíncrono do documento
    background_tasks.add_task(
        process_uploaded_bid_document,
        document_id=document.document_id,
        db=db
    )
    
    return document

@router.get("", response_model=List[DocumentPublic])
async def read_documents(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    platform: Optional[str] = None,
    type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter documentos/editais
    # Get documents/bid notices
    """
    query = select(Document)
    
    # Aplicar filtros
    if search:
        query = query.filter(
            Document.title.ilike(f"%{search}%") | 
            Document.description.ilike(f"%{search}%") | 
            Document.document_number.ilike(f"%{search}%") | 
            Document.entity.ilike(f"%{search}%")
        )
    
    if platform:
        query = query.filter(Document.platform == platform)
        
    if type:
        query = query.filter(Document.document_type == type)
    
    # Aplicar paginação
    query = query.order_by(Document.created_at.desc()).offset(skip).limit(limit)
    
    # Executar consulta
    result = await db.execute(query)
    documents = result.scalars().all()
    
    return documents

@router.get("/{document_id}", response_model=DocumentPublic)
async def read_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter um documento/edital específico
    # Get a specific document/bid notice
    """
    document = await db.get(Document, document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado."
        )
    
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    # Excluir um documento/edital
    # Delete a document/bid notice
    """
    document = await db.get(Document, document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado."
        )
    
    # Excluir arquivo físico
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        logger.error(f"Erro ao excluir arquivo: {e}")
    
    # Excluir registro no banco
    await db.delete(document)
    await db.commit()
