from pydantic import BaseModel


class EnderecoInstituicao(BaseModel):
    """Endereço da instituição"""

    endereco: str
    cep: str
