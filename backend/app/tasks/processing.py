import os
from datetime import datetime
from typing import Optional
from uuid import UUID

import structlog
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bid import Bid
from app.models.document import Document
from app.services.llm_service import analyze_document_text

# Configurar logger
# Configure logger
logger = structlog.get_logger(__name__)


async def process_uploaded_bid_document(document_id: UUID, db: AsyncSession) -> None:
    """
    # Processa um documento de licitação carregado
    # Extrair texto, analisar com LLM e atualizar resultados
    
    # Process an uploaded bid document
    # Extract text, analyze with LLM, and update results
    
    Args:
        document_id: ID do documento
        db: Sessão do banco de dados
    """
    logger.info(f"Iniciando processamento do documento {document_id}")
    
    try:
        # Atualizar status para processamento
        # Update status to processing
        stmt = select(Document).where(Document.document_id == document_id)
        result = await db.execute(stmt)
        document = result.scalars().first()
        
        if not document:
            logger.error(f"Documento {document_id} não encontrado")
            return
        
        document.processing_status = "processing"
        await db.commit()
        
        # Verificar se o arquivo existe
        # Check if file exists
        if not os.path.exists(document.file_path):
            logger.error(f"Arquivo não encontrado: {document.file_path}")
            document.processing_status = "error"
            await db.commit()
            return
        
        # Extrair texto do PDF
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(document.file_path)
        if not extracted_text:
            logger.error(f"Não foi possível extrair texto do documento {document_id}")
            document.processing_status = "error"
            await db.commit()
            return
        
        # Atualizar documento com texto extraído
        # Update document with extracted text
        document.extracted_text = extracted_text
        await db.commit()
        
        # Analisar texto com LLM
        # Analyze text with LLM
        analysis_result = await analyze_document_text(extracted_text)
        if not analysis_result:
            logger.error(f"Falha na análise LLM para o documento {document_id}")
            document.processing_status = "error"
            await db.commit()
            return
        
        # Atualizar documento com resultado da análise
        # Update document with analysis result
        document.llm_analysis = analysis_result
        document.processing_status = "completed"
        document.processed_at = datetime.utcnow()
        await db.commit()
        
        # Verificar se está associado a uma licitação e atualizar
        # Check if associated with a bid and update it
        stmt = select(Bid).where(Bid.source_document_id == document_id)
        result = await db.execute(stmt)
        bid = result.scalars().first()
        
        if bid:
            # Atualizar licitação com dados da análise
            # Update bid with analysis data
            await update_bid_from_analysis(bid, analysis_result, db)
        
        logger.info(f"Processamento do documento {document_id} concluído com sucesso")
        
    except Exception as e:
        logger.exception(f"Erro no processamento do documento {document_id}: {str(e)}")
        # Em caso de erro, atualizar status do documento
        # In case of error, update document status
        stmt = select(Document).where(Document.document_id == document_id)
        result = await db.execute(stmt)
        document = result.scalars().first()
        
        if document:
            document.processing_status = "error"
            await db.commit()


def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    # Extrai texto de um arquivo PDF
    # Extract text from a PDF file
    
    Args:
        file_path: Caminho do arquivo PDF
        
    Returns:
        str: Texto extraído ou None se falhar
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF {file_path}: {str(e)}")
        return None


async def update_bid_from_analysis(bid: Bid, analysis: dict, db: AsyncSession) -> None:
    """
    # Atualiza os dados de uma licitação com base na análise do LLM
    # Update bid data based on LLM analysis
    
    Args:
        bid: Objeto da licitação
        analysis: Resultado da análise do LLM
        db: Sessão do banco de dados
    """
    # Atualizar campos da licitação com dados da análise
    # Update bid fields with analysis data
    try:
        if analysis.get("title"):
            bid.title = analysis["title"]
        
        if analysis.get("organization"):
            bid.organization = analysis["organization"]
        
        if analysis.get("process_number"):
            bid.number = analysis["process_number"]
        
        if analysis.get("publication_date"):
            # Tentar converter string para data
            # Try to convert string to date
            try:
                bid.publication_date = datetime.fromisoformat(analysis["publication_date"])
            except ValueError:
                logger.warning(f"Data de publicação inválida: {analysis['publication_date']}")
        
        if analysis.get("bid_deadline"):
            # Tentar converter string para data
            # Try to convert string to date
            try:
                bid.deadline_date = datetime.fromisoformat(analysis["bid_deadline"])
            except ValueError:
                logger.warning(f"Data de prazo inválida: {analysis['bid_deadline']}")
        
        if analysis.get("summary"):
            bid.description = analysis["summary"]
        
        # Armazenar a análise completa em JSON
        # Store the complete analysis in JSON
        bid.analysis_result = analysis
        
        # Atualizar status da licitação para em análise
        # Update bid status to in analysis
        if bid.status == "novos":
            bid.status = "em_analise"
        
        await db.commit()
        logger.info(f"Licitação {bid.bid_id} atualizada com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao atualizar licitação com dados da análise: {str(e)}")
        # Não precisamos fazer rollback porque não estamos em uma transação explícita
        # No need to rollback as we're not in an explicit transaction
