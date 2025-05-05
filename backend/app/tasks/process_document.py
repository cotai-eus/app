import logging
from uuid import UUID
from typing import Dict, Any
import datetime

from app.db.session import AsyncSessionLocal  # Mudou de async_session_maker para AsyncSessionLocal
from app import crud, schemas
from app.services import llm_service

log = logging.getLogger(__name__)

async def process_document_task(
    response_id: UUID,
    pdf_content: bytes,
    filename: str,
    target_form_structure: Dict[str, Any],
    user_id: UUID # ID do usuário que iniciou o processo
):
    """
    Tarefa assíncrona (executada em background) para processar um PDF.

    1. Chama o serviço LLM para extrair dados do PDF com base na estrutura do formulário.
    2. Valida (basicamente) os dados extraídos.
    3. Atualiza o registro FormResponse correspondente com os dados e o status final.

    :param response_id: ID do registro FormResponse a ser atualizado.
    :param pdf_content: Conteúdo do PDF em bytes.
    :param filename: Nome original do arquivo PDF.
    :param target_form_structure: Estrutura JSON do formulário alvo.
    :param user_id: ID do usuário associado.
    """
    log.info(f"[Task {response_id}] Iniciando processamento do documento '{filename}' para o usuário {user_id}.")

    # Comentário em português: Cria uma nova sessão de banco de dados para esta tarefa.
    # É crucial usar uma sessão separada para tarefas em background.
    async with AsyncSessionLocal() as db:
        try:
            # Comentário em português: 1. Chama o serviço LLM.
            extracted_data, _ = await llm_service.extract_data_from_pdf_using_llm(
                pdf_content=pdf_content,
                target_form_structure=target_form_structure
            )

            # Comentário em português: 2. Valida os dados extraídos.
            if extracted_data is None:
                # Comentário em português: Falha na extração ou LLM. Marca como 'review_required'.
                log.warning(f"[Task {response_id}] Falha ao extrair dados do PDF '{filename}' via LLM.")
                await crud.form_response.update_status(
                    db=db,
                    response_id=response_id,
                    status='review_required',
                    processed_at=datetime.datetime.now(datetime.timezone.utc)
                )
                return # Encerra a tarefa

            # Comentário em português: Validação adicional pode ser feita aqui.
            # Ex: Verificar se os campos obrigatórios foram preenchidos, se os tipos estão corretos, etc.
            # Por simplicidade, vamos apenas aceitar o que o LLM retornou.

            # Comentário em português: 3. Atualiza o FormResponse com sucesso.
            log.info(f"[Task {response_id}] Dados extraídos com sucesso para '{filename}'. Atualizando resposta.")
            update_schema = schemas.FormResponseUpdate(
                answers=extracted_data,
                status='completed', # Marca como concluído
                processed_at=datetime.datetime.now(datetime.timezone.utc)
            )
            await crud.form_response.update(
                db=db,
                db_obj=await crud.form_response.get(db, id=response_id), # Busca o objeto para atualizar
                obj_in=update_schema
            )
            log.info(f"[Task {response_id}] Processamento do documento '{filename}' concluído com sucesso.")

        except Exception as e:
            # Comentário em português: Captura qualquer erro inesperado durante a tarefa.
            log.error(f"[Task {response_id}] Erro inesperado durante o processamento do documento '{filename}': {e}", exc_info=True)
            # Tenta marcar a resposta como 'failed' ou 'review_required' no banco.
            try:
                async with AsyncSessionLocal() as error_db: # Nova sessão para garantir
                     await crud.form_response.update_status(
                         db=error_db,
                         response_id=response_id,
                         status='failed', # Ou 'review_required'
                         processed_at=datetime.datetime.now(datetime.timezone.utc)
                     )
            except Exception as db_error:
                log.error(f"[Task {response_id}] Falha ao atualizar status para 'failed' após erro na task: {db_error}", exc_info=True)
            # A exceção será registrada, mas a tarefa termina aqui.

