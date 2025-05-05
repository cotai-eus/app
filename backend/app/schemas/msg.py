from pydantic import BaseModel

class Msg(BaseModel):
    """
    Schema genérico para retornar mensagens simples da API (e.g., sucesso, erro).
    """
    msg: str

