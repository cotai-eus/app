from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserProfile, UserProfileUpdate
from app.core.config import settings

router = APIRouter()

@router.get("", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Obter perfil do usuário atual
    # Get current user profile
    """
    # Retorna os dados do perfil atual
    return {
        "id": str(current_user.user_id),
        "nome": current_user.full_name,
        "email": current_user.email,
        "cpf": "",  # Mock - em ambiente real viria de um modelo relacionado
        "telefone": "",  # Mock - em ambiente real viria de um modelo relacionado
        "cargo": "",  # Mock - em ambiente real viria de um modelo relacionado
        "departamento": "",  # Mock - em ambiente real viria de um modelo relacionado
        "avatarUrl": current_user.avatar_url
    }

@router.put("", response_model=UserProfile)
async def update_profile(
    *,
    db: AsyncSession = Depends(get_db),
    profile_update: UserProfileUpdate = Body(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar perfil do usuário atual
    # Update current user profile
    """
    # Atualizar campos básicos do usuário
    current_user.full_name = profile_update.nome
    
    # Verificar se o email está sendo alterado
    if profile_update.email != current_user.email:
        # Em implementação real, verificaríamos se o email já está em uso
        # e faríamos validação adicional (envio de código, etc.)
        current_user.email = profile_update.email
    
    # Atualizar campos adicionais
    # Em ambiente real, isso seria salvo em modelos relacionados
    
    # Salvar alterações
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    
    # Retornar perfil atualizado
    return {
        "id": str(current_user.user_id),
        "nome": current_user.full_name,
        "email": current_user.email,
        "cpf": profile_update.cpf,
        "telefone": profile_update.telefone,
        "cargo": profile_update.cargo,
        "departamento": profile_update.departamento,
        "avatarUrl": current_user.avatar_url
    }

@router.post("/avatar", response_model=dict)
async def update_avatar(
    *,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    # Atualizar avatar do usuário
    # Update user avatar
    """
    # Verificar tipo do arquivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo deve ser uma imagem"
        )
    
    # Criar diretório de uploads se não existir
    avatar_dir = os.path.join(settings.UPLOAD_DIRECTORY, "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    
    # Gerar nome de arquivo único
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Caminho completo
    file_path = os.path.join(avatar_dir, filename)
    
    # URL relativa para acessar o avatar
    avatar_url = f"/uploads/avatars/{filename}"
    
    # Salvar arquivo
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Atualizar URL do avatar no banco
    current_user.avatar_url = avatar_url
    db.add(current_user)
    await db.commit()
    
    return {"avatar_url": avatar_url}
