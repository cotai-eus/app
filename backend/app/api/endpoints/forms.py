from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from uuid import UUID
import logging

from app import crud, models, schemas
from app.api import deps

router = APIRouter()
log = logging.getLogger(__name__)

# --- Endpoints para Gerenciar Templates de Formulários (Forms) ---
# Assumindo que são globais e gerenciados por admins

@router.post("/templates", response_model=schemas.Form, status_code=status.HTTP_201_CREATED)
async def create_form_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    form_in: schemas.FormCreate,
    current_user: models.User = Depends(deps.get_current_active_admin), # Requer admin
) -> Any:
    """
    Cria um novo template de formulário (requer admin).
    """
    # Comentário em português: Cria o template de formulário usando o CRUD.
    form_template = await crud.form.create(db=db, obj_in=form_in)
    log.info(f"Admin {current_user.email} criou template de formulário {form_template.form_id} ('{form_template.title}')")
    return form_template

@router.get("/templates", response_model=List[schemas.Form])
async def read_form_templates(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    # current_user: models.User = Depends(deps.get_current_active_user), # Qualquer usuário pode listar?
) -> Any:
    """
    Obtém a lista de templates de formulário disponíveis.
    (Aberto para qualquer usuário logado por padrão, ajuste se necessário).
    """
    # Comentário em português: Busca os templates de formulário com paginação.
    form_templates = await crud.form.get_multi(db=db, skip=skip, limit=limit)
    return form_templates

@router.get("/templates/{form_id}", response_model=schemas.Form)
async def read_form_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    form_id: UUID,
    # current_user: models.User = Depends(deps.get_current_active_user), # Qualquer usuário pode ver?
) -> Any:
    """
    Obtém um template de formulário específico pelo ID.
    """
    # Comentário em português: Busca o template pelo ID.
    form_template = await crud.form.get(db=db, id=form_id)
    if not form_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template de formulário não encontrado")
    return form_template

@router.put("/templates/{form_id}", response_model=schemas.Form)
async def update_form_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    form_id: UUID,
    form_in: schemas.FormUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin), # Requer admin
) -> Any:
    """
    Atualiza um template de formulário existente (requer admin).
    """
    # Comentário em português: Busca o template a ser atualizado.
    form_template = await crud.form.get(db=db, id=form_id)
    if not form_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template de formulário não encontrado")

    # Comentário em português: Atualiza o template usando o CRUD.
    updated_form_template = await crud.form.update(db=db, db_obj=form_template, obj_in=form_in)
    log.info(f"Admin {current_user.email} atualizou template de formulário {form_id}")
    return updated_form_template

@router.delete("/templates/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    form_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_admin), # Requer admin
) -> None:
    """
    Exclui um template de formulário (requer admin).
    Isso também excluirá todas as respostas associadas (ON DELETE CASCADE).
    """
    # Comentário em português: Busca o template a ser excluído.
    form_template = await crud.form.get(db=db, id=form_id)
    if not form_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template de formulário não encontrado")

    # Comentário em português: Remove o template usando o CRUD.
    await crud.form.remove(db=db, id=form_id)
    log.info(f"Admin {current_user.email} excluiu template de formulário {form_id}")
    # Retorna 204 No Content


# --- Endpoints para Gerenciar Respostas de Formulários (FormResponses) ---

@router.post("/responses", response_model=schemas.FormResponse, status_code=status.HTTP_201_CREATED)
async def submit_form_response(
    *,
    db: AsyncSession = Depends(deps.get_db),
    response_in: schemas.FormResponseCreate, # Schema já inclui form_id e user_id
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submete uma nova resposta para um formulário.
    O user_id no payload deve corresponder ao usuário autenticado (ou ser admin?).
    """
    # Comentário em português: Valida se o form_id existe.
    form_template = await crud.form.get(db=db, id=response_in.form_id)
    if not form_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formulário (template) não encontrado.")

    # Comentário em português: Valida se o user_id na resposta corresponde ao usuário logado (ou se é admin).
    if response_in.user_id != current_user.user_id and not current_user.is_admin:
         log.warning(f"Usuário {current_user.email} tentou submeter resposta para usuário {response_in.user_id}")
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a submeter resposta para este usuário.")

    # Comentário em português: Valida se o user_id existe (caso um admin esteja submetendo por outro).
    if response_in.user_id != current_user.user_id:
        target_user = await crud.user.get(db=db, id=response_in.user_id)
        if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário alvo da resposta não encontrado.")

    # TODO: Validação mais robusta das 'answers' contra a 'structure' do formulário.
    # Isso pode envolver verificar se todos os campos obrigatórios estão presentes,
    # se os tipos de dados correspondem, etc.

    # Comentário em português: Cria a resposta usando o CRUD.
    # Define o status inicial (pode ser 'completed' se submissão manual, ou 'pending'/'processing' se via AI)
    response_in.status = response_in.status or 'completed' # Default para 'completed' se não especificado
    form_response = await crud.form_response.create_with_form_and_user(db=db, obj_in=response_in)
    log.info(f"Resposta {form_response.response_id} submetida para formulário {response_in.form_id} por usuário {response_in.user_id}")
    return form_response


@router.get("/responses", response_model=List[schemas.FormResponse])
async def read_form_responses(
    *,
    db: AsyncSession = Depends(deps.get_db),
    form_id: UUID = Query(None, description="Filtrar respostas por ID do formulário"),
    user_id: UUID = Query(None, description="Filtrar respostas por ID do usuário (requer admin se não for o próprio usuário)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém uma lista de respostas de formulários.
    Pode filtrar por form_id ou user_id.
    Acesso a respostas de outros usuários requer privilégios de admin.
    """
    if user_id and user_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a ver respostas de outros usuários.")

    target_user_id = user_id if user_id else current_user.user_id if not current_user.is_admin else None

    # Comentário em português: Decide qual método CRUD usar baseado nos filtros.
    if form_id:
        # TODO: Adicionar filtro por user_id também em get_multi_by_form se necessário
        responses = await crud.form_response.get_multi_by_form(db=db, form_id=form_id, skip=skip, limit=limit)
        # Filtrar por usuário após a busca se necessário (menos eficiente)
        if target_user_id:
            responses = [r for r in responses if r.user_id == target_user_id]
    elif target_user_id:
        responses = await crud.form_response.get_multi_by_user(db=db, user_id=target_user_id, skip=skip, limit=limit)
    elif current_user.is_admin: # Admin buscando todas as respostas (sem filtro de usuário)
         # Precisa de um get_multi geral no CRUDFormResponse ou usar o base
         base_crud = crud.base.CRUDBase(models.FormResponse)
         responses = await base_crud.get_multi(db=db, skip=skip, limit=limit)
         # Ordenar se necessário: responses.sort(key=lambda r: r.submitted_at, reverse=True)
    else:
        # Usuário não admin buscando suas próprias respostas (sem filtro de form_id)
        responses = await crud.form_response.get_multi_by_user(db=db, user_id=current_user.user_id, skip=skip, limit=limit)

    return responses


@router.get("/responses/{response_id}", response_model=schemas.FormResponse)
async def read_form_response(
    *,
    db: AsyncSession = Depends(deps.get_db),
    response_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtém uma resposta de formulário específica pelo ID.
    """
    # Comentário em português: Busca a resposta pelo ID.
    response = await crud.form_response.get(db=db, id=response_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resposta de formulário não encontrada")
    # Comentário em português: Verifica se a resposta pertence ao usuário logado ou se é admin.
    if response.user_id != current_user.user_id and not current_user.is_admin:
        log.warning(f"Usuário {current_user.email} tentou acessar resposta {response_id} de outro usuário.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")
    return response

@router.get("/responses/{response_id}/status", response_model=schemas.FormResponseStatus)
async def get_form_response_status(
    *,
    db: AsyncSession = Depends(deps.get_db),
    response_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Verifica o status de processamento de uma resposta de formulário.
    Útil para polling após submissão de processamento AI.
    """
    # Comentário em português: Busca a resposta pelo ID.
    response = await crud.form_response.get(db=db, id=response_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resposta de formulário não encontrada")
    # Comentário em português: Verifica permissão.
    if response.user_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Retorna apenas os campos relevantes para o status.
    return response # O schema FormResponseStatus selecionará os campos corretos


@router.put("/responses/{response_id}", response_model=schemas.FormResponse)
async def update_form_response(
    *,
    db: AsyncSession = Depends(deps.get_db),
    response_id: UUID,
    response_in: schemas.FormResponseUpdate, # Schema para atualização (status, answers, processed_at)
    current_user: models.User = Depends(deps.get_current_active_user), # Ou admin?
) -> Any:
    """
    Atualiza uma resposta de formulário existente.
    (Usado principalmente internamente pelo processo AI ou por admins para correção).
    """
    # Comentário em português: Busca a resposta a ser atualizada.
    response = await crud.form_response.get(db=db, id=response_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resposta de formulário não encontrada")
    # Comentário em português: Verifica permissão (admin ou talvez o próprio usuário possa corrigir?).
    if response.user_id != current_user.user_id and not current_user.is_admin:
        log.warning(f"Usuário {current_user.email} tentou atualizar resposta {response_id} não autorizada.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Atualiza a resposta usando o CRUD.
    # Adiciona a data de processamento se o status for alterado para um estado final.
    if response_in.status and response_in.status in ['completed', 'review_required'] and not response.processed_at:
         response_in.processed_at = datetime.datetime.now(datetime.timezone.utc)

    updated_response = await crud.form_response.update(db=db, db_obj=response, obj_in=response_in)
    log.info(f"Usuário {current_user.email} atualizou resposta {response_id}")
    return updated_response


@router.delete("/responses/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form_response(
    *,
    db: AsyncSession = Depends(deps.get_db),
    response_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user), # Ou admin?
) -> None:
    """
    Exclui uma resposta de formulário.
    """
    # Comentário em português: Busca a resposta a ser excluída.
    response = await crud.form_response.get(db=db, id=response_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resposta de formulário não encontrada")
    # Comentário em português: Verifica permissão (próprio usuário ou admin).
    if response.user_id != current_user.user_id and not current_user.is_admin:
        log.warning(f"Usuário {current_user.email} tentou excluir resposta {response_id} não autorizada.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")

    # Comentário em português: Remove a resposta usando o CRUD.
    await crud.form_response.remove(db=db, id=response_id)
    log.info(f"Usuário {current_user.email} excluiu resposta {response_id}")
    # Retorna 204 No Content

