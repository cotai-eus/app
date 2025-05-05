import os
import uuid
from pathlib import Path
from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.crud.base import CRUDBase
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentPublic, DocumentWithAnalysis
from app.tasks.processing import process_uploaded_bid_document

router = APIRouter()

# Criar instância CRUD para documentos
# Create CRUD instance for documents
crud_document = CRUDBase(Document)


@router.post("/upload", response_model=DocumentPublic)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Enviar um novo documento
    # Upload a new document
    
    Args:
        background_tasks: Tarefas em segundo plano do FastAPI
        file: Arquivo enviado
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        O documento criado
    """
    # Verificar tipo de arquivo (aceitar apenas PDF)
    # Check file type (accept only PDF)
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF são aceitos",
        )
    
    # Criar diretório de upload se não existir
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIRECTORY) / str(current_user.user_id)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único para o arquivo
    # Generate unique name for the file
    file_id = uuid.uuid4()
    file_extension = os.path.splitext(file.filename)[1]
    file_path = upload_dir / f"{file_id}{file_extension}"
    
    # Salvar arquivo
    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Criar registro do documento no banco de dados
    # Create document record in database
    document_in = DocumentCreate(
        file_name=file.filename,
        file_path=str(file_path),
        content_type=file.content_type,
        size_bytes=len(contents),
        processing_status="pending"
    )
    
    document_data = document_in.model_dump()
    document_data["user_id"] = current_user.user_id
    
    # Criar o documento
    # Create the document
    db_document = Document(**document_data)
    db.add(db_document)
    await db.commit()
    await db.refresh(db_document)
    
    # Iniciar processamento do documento em segundo plano
    # Start document processing in background
    background_tasks.add_task(
        process_uploaded_bid_document, 
        document_id=db_document.document_id, 
        db=db
    )
    
    return db_document


@router.get("", response_model=List[DocumentPublic])
async def read_documents(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter documentos do usuário atual
    # Get documents of the current user
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        current_user: Usuário atual obtido do token
        
    Returns:
        Lista de documentos
    """
    # Filtrar documentos pelo ID do usuário atual
    # Filter documents by current user ID
    stmt = select(Document).where(
        Document.user_id == current_user.user_id
    ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{document_id}", response_model=DocumentWithAnalysis)
async def read_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter detalhes de um documento específico
    # Get details of a specific document
    
    Args:
        document_id: ID do documento
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Detalhes do documento solicitado
    """
    document = await crud_document.get(db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado",
        )
    
    # Verificar se o documento pertence ao usuário atual
    # Check if the document belongs to the current user
    if document.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este documento",
        )
    
    return document


@router.get("/{document_id}/status", response_model=DocumentPublic)
async def check_document_status(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Verificar o status de processamento de um documento
    # Check the processing status of a document
    
    Args:
        document_id: ID do documento
        db: Sessão do banco de dados
        current_user: Usuário atual obtido do token
        
    Returns:
        Status de processamento do documento
    """
    document = await crud_document.get(db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado",
        )
    
    # Verificar se o documento pertence ao usuário atual
    # Check if the document belongs to the current user
    if document.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado a este documento",
        )
    
    return document
