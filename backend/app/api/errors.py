from fastapi import HTTPException, status

class APIException(HTTPException):
    """
    Classe base para exceções da API.
    
    Estende a HTTPException do FastAPI para ter mais controle
    sobre os erros retornados pela API.
    """
    def __init__(
        self,
        status_code: int,
        detail: str = None,
        headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(APIException):
    """
    Exceção para recursos não encontrados.
    """
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictException(APIException):
    """
    Exceção para conflitos (ex: recurso já existe).
    """
    def __init__(self, detail: str = "Conflito ao criar ou atualizar recurso"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class BadRequestException(APIException):
    """
    Exceção para solicitações inválidas.
    """
    def __init__(self, detail: str = "Parâmetros inválidos"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(APIException):
    """
    Exceção para autenticação falha.
    """
    def __init__(self, detail: str = "Autenticação necessária"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(APIException):
    """
    Exceção para usuários sem permissão.
    """
    def __init__(self, detail: str = "Permissão negada"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ProcessingException(APIException):
    """
    Exceção para erros de processamento.
    """
    def __init__(self, detail: str = "Erro ao processar a solicitação"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)