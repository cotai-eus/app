import httpx
import logging
from typing import Dict, Any, Optional, Tuple
import json
import PyPDF2 # Usado para extração básica de texto do PDF
import io
import structlog

from app.core.config import settings

log = logging.getLogger(__name__)

# Configurar logger
logger = structlog.get_logger(__name__)

# --- Configuração do Cliente HTTPX ---
# Cria um cliente HTTPX assíncrono reutilizável com timeouts configurados
# Timeouts: connect=5s, read=30s, write=10s, pool=5s
# Limits: max_connections=100, max_keepalive_connections=20
# Follow redirects: True
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(30.0, connect=5.0, read=60.0, write=10.0), # Aumentado read timeout para LLM
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    follow_redirects=True,
    http2=True, # Tenta usar HTTP/2 se suportado
)

# --- Funções de Extração de Texto ---

async def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extrai texto de um conteúdo de PDF em bytes usando PyPDF2.
    Esta é uma extração básica, pode não funcionar bem com layouts complexos ou PDFs baseados em imagem.
    Para cenários mais robustos, considere OCR ou serviços especializados.

    :param pdf_content: Conteúdo do PDF em bytes.
    :return: Texto extraído ou string vazia se falhar.
    """
    # Comentário em português: Tenta extrair texto do PDF usando PyPDF2.
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        num_pages = len(pdf_reader.pages)
        log.debug(f"Extraindo texto de PDF com {num_pages} páginas.")
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n" # Adiciona nova linha entre páginas
        log.info(f"Texto extraído do PDF com sucesso ({len(text)} caracteres).")
        return text.strip()
    except Exception as e:
        log.error(f"Falha ao extrair texto do PDF com PyPDF2: {e}", exc_info=True)
        # Comentário em português: Retorna vazio em caso de erro na extração.
        return ""

# --- Funções de Interação com LLM ---

async def call_llm_api(prompt: str, max_tokens: int = 1024) -> Optional[Dict[str, Any]]:
    """
    Chama a API do LLM configurada (OpenAI, Gemini, etc.) com o prompt fornecido.

    :param prompt: O prompt a ser enviado para o LLM.
    :param max_tokens: Número máximo de tokens a serem gerados na resposta.
    :return: O JSON da resposta do LLM ou None em caso de erro.
    """
    # Comentário em português: Verifica se a chave da API está configurada.
    if not settings.LLM_API_KEY:
        log.error("Chave da API do LLM (LLM_API_KEY) não configurada.")
        return None

    provider = settings.LLM_PROVIDER.lower()
    api_key = settings.LLM_API_KEY
    model = settings.LLM_MODEL_NAME

    headers = {
        "Content-Type": "application/json",
    }
    payload = {}
    url = ""

    # Comentário em português: Monta a requisição específica para o provedor configurado.
    if provider == "openai":
        if not model: model = "gpt-4o" # Modelo padrão OpenAI se não especificado
        url = "https://api.openai.com/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.2, # Baixa temperatura para respostas mais determinísticas (JSON)
            "response_format": {"type": "json_object"} # Solicita explicitamente JSON (modelos suportados)
        }
        log.debug(f"Chamando API OpenAI: {url} com modelo {model}")

    elif provider == "gemini":
        if not model: model = "gemini-pro" # Modelo padrão Gemini se não especificado
        # Nota: A API do Gemini pode ter URLs e estruturas de payload diferentes.
        # Este é um exemplo genérico, ajuste conforme a documentação oficial.
        # url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}" # Exemplo URL v1
        # Gemini pode esperar um formato diferente, como 'contents'
        payload = {
             "contents": [{"parts":[{"text": prompt}]}],
             "generationConfig": {
                 "responseMimeType": "application/json", # Solicita JSON
                 "maxOutputTokens": max_tokens,
                 "temperature": 0.2,
             }
        }
        log.debug(f"Chamando API Gemini: {url} com modelo {model}")

    else:
        log.error(f"Provedor LLM não suportado: {provider}")
        return None

    try:
        # Comentário em português: Faz a requisição POST assíncrona para a API do LLM.
        response = await http_client.post(url, headers=headers, json=payload)
        response.raise_for_status() # Levanta exceção para status HTTP 4xx/5xx

        response_json = response.json()
        log.info(f"Resposta recebida com sucesso da API {provider}.")
        log.debug(f"Resposta JSON da API {provider}: {response_json}") # Loga a resposta completa para debug
        return response_json

    except httpx.RequestError as e:
        log.error(f"Erro de requisição ao chamar API {provider} em {url}: {e}", exc_info=True)
        return None
    except httpx.HTTPStatusError as e:
        log.error(f"Erro HTTP ao chamar API {provider}: Status {e.response.status_code}, Resposta: {e.response.text}", exc_info=True)
        return None
    except json.JSONDecodeError as e:
        log.error(f"Erro ao decodificar JSON da resposta da API {provider}: {e}", exc_info=True)
        return None
    except Exception as e:
        log.error(f"Erro inesperado ao chamar API {provider}: {e}", exc_info=True)
        return None


def parse_llm_response(response_json: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extrai o conteúdo JSON relevante da resposta da API do LLM.
    Adapta a extração com base no provedor.

    :param response_json: O JSON completo da resposta da API.
    :return: O dicionário JSON extraído ou None se não puder ser encontrado/parseado.
    """
    provider = settings.LLM_PROVIDER.lower()
    extracted_json_str = None

    try:
        # Comentário em português: Tenta extrair o conteúdo da resposta baseado no provedor.
        if provider == "openai":
            # Exemplo: {"choices": [{"message": {"role": "assistant", "content": "{\"key\": \"value\"}"}}]}
            extracted_json_str = response_json.get("choices", [{}])[0].get("message", {}).get("content")
        elif provider == "gemini":
            # Exemplo (pode variar): {"candidates": [{"content": {"parts": [{"text": "```json\n{\"key\": \"value\"}\n```"}]}}]}
            # Gemini pode retornar o JSON dentro de blocos de código markdown.
            raw_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
            if raw_text:
                # Remove ```json e ``` do início e fim, se presentes
                if raw_text.strip().startswith("```json"):
                    extracted_json_str = raw_text.strip()[7:-3].strip()
                elif raw_text.strip().startswith("```"):
                     extracted_json_str = raw_text.strip()[3:-3].strip()
                else:
                    extracted_json_str = raw_text.strip() # Assume que é JSON direto
        else:
            log.warning(f"Parser não implementado para o provedor LLM: {provider}")
            return None

        if not extracted_json_str:
            log.warning(f"Não foi possível extrair conteúdo JSON da resposta do LLM ({provider}). Resposta: {response_json}")
            return None

        # Comentário em português: Tenta decodificar a string JSON extraída.
        parsed_data = json.loads(extracted_json_str)
        if not isinstance(parsed_data, dict):
             log.warning(f"Conteúdo extraído do LLM não é um dicionário JSON: {parsed_data}")
             return None

        log.info("JSON extraído com sucesso da resposta do LLM.")
        return parsed_data

    except (IndexError, KeyError, TypeError) as e:
        log.error(f"Erro ao acessar estrutura esperada na resposta do LLM ({provider}): {e}. Resposta: {response_json}", exc_info=True)
        return None
    except json.JSONDecodeError as e:
        log.error(f"Erro ao decodificar a string JSON extraída da resposta do LLM ({provider}): {e}. String: '{extracted_json_str}'", exc_info=True)
        return None
    except Exception as e:
        log.error(f"Erro inesperado ao parsear resposta do LLM ({provider}): {e}", exc_info=True)
        return None


async def extract_data_from_pdf_using_llm(
    pdf_content: bytes,
    target_form_structure: Dict[str, Any]
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Orquestra a extração de dados de um PDF usando LLM.
    1. Extrai texto do PDF.
    2. Constrói um prompt para o LLM pedindo para preencher o formulário.
    3. Chama a API do LLM.
    4. Parseia a resposta JSON do LLM.

    :param pdf_content: Conteúdo do PDF em bytes.
    :param target_form_structure: Estrutura do formulário alvo (JSON).
    :return: Uma tupla contendo (dicionário com dados extraídos ou None, texto bruto extraído do PDF ou None).
    """
    # Comentário em português: 1. Extrai texto do PDF.
    extracted_text = await extract_text_from_pdf(pdf_content)
    if not extracted_text:
        log.warning("Não foi possível extrair texto do PDF. Abortando processamento LLM.")
        return None, None

    # Comentário em português: 2. Constrói o prompt.
    # O prompt deve instruir o LLM a extrair informações do texto
    # e formatá-las como um JSON que corresponda aos campos esperados pelo formulário.
    # Exemplo simples de prompt:
    form_fields_description = json.dumps(target_form_structure.get("fields", []), indent=2) # Descreve os campos esperados
    prompt = f"""
    Analise o seguinte texto extraído de um documento PDF e preencha os campos do formulário descrito abaixo.
    Responda APENAS com um objeto JSON contendo os pares chave-valor correspondentes aos campos do formulário.
    Se uma informação para um campo não for encontrada no texto, omita o campo ou use um valor nulo (null).
    Não inclua explicações adicionais, apenas o JSON.

    Estrutura do Formulário (campos esperados):
    {form_fields_description}

    Texto Extraído do PDF:
    --- INÍCIO DO TEXTO ---
    {extracted_text[:8000]}
    --- FIM DO TEXTO ---

    JSON Resultante:
    """
    # Limitamos o texto enviado para evitar exceder limites de token do LLM.
    # Uma abordagem mais sofisticada poderia usar técnicas de chunking ou RAG.

    log.debug(f"Prompt construído para o LLM (primeiros 500 chars): {prompt[:500]}...")

    # Comentário em português: 3. Chama a API do LLM.
    llm_response_json = await call_llm_api(prompt)
    if not llm_response_json:
        log.error("Falha ao obter resposta da API do LLM.")
        return None, extracted_text # Retorna o texto extraído mesmo se o LLM falhar

    # Comentário em português: 4. Parseia a resposta JSON do LLM.
    extracted_data = parse_llm_response(llm_response_json)
    if not extracted_data:
        log.error("Falha ao parsear o JSON da resposta do LLM.")
        return None, extracted_text

    log.info(f"Dados extraídos com sucesso pelo LLM: {extracted_data}")
    return extracted_data, extracted_text


async def analyze_document_text(text: str) -> Optional[Dict]:
    """
    # Analisa o texto de um documento usando uma API de LLM
    # Analyzes document text using an LLM API
    
    Args:
        text: Texto extraído do documento
        
    Returns:
        Dict: Resultado da análise ou None se houver erro
    """
    logger.info("Iniciando análise de documento com LLM")
    
    # Selecionar o provedor LLM com base nas configurações
    # Select LLM provider based on settings
    if settings.LLM_PROVIDER == "openai":
        return await analyze_with_openai(text)
    elif settings.LLM_PROVIDER == "gemini":
        return await analyze_with_gemini(text)
    else:
        logger.error(f"Provedor LLM não suportado: {settings.LLM_PROVIDER}")
        return None


async def analyze_with_openai(text: str) -> Optional[Dict]:
    """
    # Analisa o texto usando a API OpenAI
    # Analyzes text using the OpenAI API
    
    Args:
        text: Texto a ser analisado
        
    Returns:
        Dict: Resultado da análise ou None se houver erro
    """
    # Truncar o texto se for muito longo (limite do OpenAI)
    # Truncate text if too long (OpenAI limit)
    max_length = 15000
    truncated_text = text[:max_length] if len(text) > max_length else text
    
    # Construir prompt para o LLM
    # Build prompt for the LLM
    prompt = f"""
    Você é um especialista em análise de editais de licitação. 
    Analise o seguinte texto de um edital e extraia as seguintes informações no formato JSON:
    
    1. title: Título/objeto da licitação
    2. organization: Nome da organização/órgão licitante
    3. process_number: Número do processo
    4. publication_date: Data de publicação (formato YYYY-MM-DD, se disponível)
    5. bid_deadline: Data limite para envio de propostas (formato YYYY-MM-DD, se disponível)
    6. contact_email: Email de contato (se disponível)
    7. contact_phone: Telefone de contato (se disponível)
    8. estimated_value: Valor estimado da licitação (se disponível)
    9. requirements: Lista das principais exigências técnicas
    10. summary: Resumo conciso da licitação (até 200 caracteres)
    
    Texto do edital:
    {truncated_text}
    
    Responda APENAS com o JSON, sem texto adicional.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.LLM_API_KEY}"
            }
            
            payload = {
                "model": settings.LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "Você é um assistente especializado em análise de editais de licitação."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "response_format": {"type": "json_object"}
            }
            
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extrair e parsear o resultado JSON
            # Extract and parse JSON result
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
    
    except (httpx.RequestError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Erro na análise com OpenAI: {str(e)}")
        return None


async def analyze_with_gemini(text: str) -> Optional[Dict]:
    """
    # Analisa o texto usando a API Gemini do Google
    # Analyzes text using Google's Gemini API
    
    Args:
        text: Texto a ser analisado
        
    Returns:
        Dict: Resultado da análise ou None se houver erro
    """
    # Truncar o texto se for muito longo (limite do Gemini)
    # Truncate text if too long (Gemini limit)
    max_length = 15000
    truncated_text = text[:max_length] if len(text) > max_length else text
    
    # Construir prompt para o LLM
    # Build prompt for the LLM
    prompt = f"""
    Você é um especialista em análise de editais de licitação. 
    Analise o seguinte texto de um edital e extraia as seguintes informações no formato JSON:
    
    1. title: Título/objeto da licitação
    2. organization: Nome da organização/órgão licitante
    3. process_number: Número do processo
    4. publication_date: Data de publicação (formato YYYY-MM-DD, se disponível)
    5. bid_deadline: Data limite para envio de propostas (formato YYYY-MM-DD, se disponível)
    6. contact_email: Email de contato (se disponível)
    7. contact_phone: Telefone de contato (se disponível)
    8. estimated_value: Valor estimado da licitação (se disponível)
    9. requirements: Lista das principais exigências técnicas
    10. summary: Resumo conciso da licitação (até 200 caracteres)
    
    Texto do edital:
    {truncated_text}
    
    Responda APENAS com o JSON, sem texto adicional.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            # URL da API Gemini
            # Gemini API URL
            api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={settings.LLM_API_KEY}"
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0,
                    "topP": 1,
                    "topK": 1
                }
            }
            
            response = await client.post(
                api_url,
                json=payload,
                timeout=60.0
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extrair e parsear o resultado
            # Extract and parse the result
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(content)
    
    except (httpx.RequestError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Erro na análise com Gemini: {str(e)}")
        return None

