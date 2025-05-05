from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Form as FastApiForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from uuid import UUID
import logging
import io

from app import crud, models, schemas
from app.api import deps
from app.tasks.process_document import process_document_task # Importa a função da task

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/process", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Msg)
async def process_document_for_form_filling(
    *,
    db: AsyncSession = Depends(deps.get_db),
    background_tasks: BackgroundTasks,
    target_form_id: UUID = FastApiForm(..., description="ID do template de formulário alvo para preenchimento"),
    pdf_file: UploadFile = File(..., description="Arquivo PDF a ser processado"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Recebe um upload de arquivo PDF e um ID de formulário alvo.
    Inicia uma tarefa em background para processar o PDF usando IA,
    extrair dados e tentar preencher o formulário correspondente.

    Retorna imediatamente com status 202 Accepted. O status do processamento
    pode ser verificado no endpoint de status da resposta do formulário.
    """
    # Comentário em português: Verifica se o formulário alvo existe.
    target_form = await crud.form.get(db=db, id=target_form_id)
    if not target_form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formulário alvo não encontrado.")

    # Comentário em português: Valida o tipo de arquivo (básico).
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de arquivo inválido. Apenas PDF é aceito.")

    # Comentário em português: Lê o conteúdo do arquivo em memória.
    # Para arquivos grandes, considerar streaming ou salvar em disco/storage temporário.
    try:
        pdf_content = await pdf_file.read()
        if not pdf_content:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo PDF vazio.")
        log.info(f"Recebido arquivo PDF '{pdf_file.filename}' ({len(pdf_content)} bytes) para processamento no formulário {target_form_id} pelo usuário {current_user.email}")
    except Exception as e:
        log.error(f"Erro ao ler arquivo PDF '{pdf_file.filename}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao ler o arquivo PDF.")
    finally:
        await pdf_file.close()

    # Comentário em português: Cria um registro inicial de FormResponse com status 'pending' ou 'processing'.
    # Isso nos dá um ID para rastrear o progresso.
    initial_response_data = schemas.FormResponseCreate(
        form_id=target_form_id,
        user_id=current_user.user_id,
        answers={}, # Respostas vazias inicialmente
        status='processing', # Define como 'processing'
        # source_pdf_id=... # Se tivéssemos uma tabela 'documents', salvaríamos o PDF e linkaríamos aqui.
    )
    try:
        form_response = await crud.form_response.create_with_form_and_user(db=db, obj_in=initial_response_data)
        log.info(f"Registro FormResponse {form_response.response_id} criado para rastrear processamento do PDF '{pdf_file.filename}'.")
    except Exception as e:
        await db.rollback()
        log.error(f"Erro ao criar registro FormResponse inicial para PDF '{pdf_file.filename}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao iniciar o processamento do documento.")


    # Comentário em português: Adiciona a tarefa de processamento à fila de background tasks do FastAPI.
    # Passa os dados necessários para a tarefa.
    background_tasks.add_task(
        process_document_task,
        response_id=form_response.response_id,
        pdf_content=pdf_content,
        filename=pdf_file.filename, # Passa o nome do arquivo original
        target_form_structure=target_form.structure, # Passa a estrutura do formulário alvo
        user_id=current_user.user_id
    )

    # Comentário em português: Retorna 202 Accepted indicando que a tarefa foi iniciada.
    # O cliente deve usar o response_id para verificar o status posteriormente.
    return {"msg": f"Processamento do documento iniciado. Verifique o status usando o ID da resposta: {form_response.response_id}"}

